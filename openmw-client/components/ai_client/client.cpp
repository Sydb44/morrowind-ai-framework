#include "client.hpp"

#include <iostream>
#include <chrono>
#include <random>
#include <sstream>
#include <iomanip>
#include <nlohmann/json.hpp>

namespace AI
{
    using json = nlohmann::json;
    namespace beast = boost::beast;
    namespace websocket = beast::websocket;
    namespace net = boost::asio;
    using tcp = net::ip::tcp;

    Client::Client(const std::string& host, unsigned short port)
        : mHost(host)
        , mPort(port)
        , mConnected(false)
        , mRunning(false)
    {
    }

    Client::~Client()
    {
        disconnect();
    }

    bool Client::connect()
    {
        if (mConnected)
            return true;

        try
        {
            // Create resolver and websocket
            mResolver = std::make_unique<tcp::resolver>(mIoContext);
            mWebSocket = std::make_unique<websocket::stream<tcp::socket>>(mIoContext);

            // Look up the domain name
            auto const results = mResolver->resolve(mHost, std::to_string(mPort));

            // Connect to the server
            net::connect(mWebSocket->next_layer(), results.begin(), results.end());

            // Perform the websocket handshake
            mWebSocket->handshake(mHost, "/");

            // Set connected flag
            mConnected = true;
            mRunning = true;

            // Start IO thread
            mIoThread = std::thread(&Client::runIoContext, this);

            return true;
        }
        catch (const std::exception& e)
        {
            std::cerr << "Error connecting to AI server: " << e.what() << std::endl;
            return false;
        }
    }

    void Client::disconnect()
    {
        if (!mConnected)
            return;

        try
        {
            // Set running flag to false
            mRunning = false;

            // Close the websocket connection
            mWebSocket->close(websocket::close_code::normal);

            // Wait for IO thread to finish
            if (mIoThread.joinable())
                mIoThread.join();

            // Reset websocket and resolver
            mWebSocket.reset();
            mResolver.reset();

            // Set connected flag to false
            mConnected = false;
        }
        catch (const std::exception& e)
        {
            std::cerr << "Error disconnecting from AI server: " << e.what() << std::endl;
        }
    }

    bool Client::isConnected() const
    {
        return mConnected;
    }

    void Client::sendDialogueRequest(
        const std::string& npcId,
        const std::string& npcName,
        const std::string& npcRace,
        const std::string& npcGender,
        const std::string& npcClass,
        const std::string& npcFaction,
        const std::string& playerMessage,
        const std::map<std::string, std::string>& gameState,
        DialogueCallback callback)
    {
        if (!mConnected)
        {
            if (!connect())
            {
                callback("Error: Not connected to AI server", {});
                return;
            }
        }

        // Generate request ID
        std::string requestId = generateRequestId();

        // Create JSON request
        json request;
        request["type"] = "dialogue";
        request["requestId"] = requestId;
        request["npc"] = {
            {"id", npcId},
            {"name", npcName},
            {"race", npcRace},
            {"gender", npcGender},
            {"class", npcClass},
            {"faction", npcFaction}
        };
        request["playerMessage"] = playerMessage;
        request["gameState"] = gameState;

        // Convert to string
        std::string requestStr = request.dump();

        // Store callback
        {
            std::lock_guard<std::mutex> lock(mMutex);
            mDialogueCallbacks[requestId] = callback;
        }

        // Add to request queue
        {
            std::lock_guard<std::mutex> lock(mMutex);
            mRequestQueue.push({requestStr, [this, requestId](const std::string& response) {
                try
                {
                    // Parse response
                    json responseJson = json::parse(response);

                    // Check for error
                    if (responseJson.contains("error"))
                    {
                        std::string error = responseJson["error"];
                        std::lock_guard<std::mutex> lock(mMutex);
                        auto it = mDialogueCallbacks.find(requestId);
                        if (it != mDialogueCallbacks.end())
                        {
                            it->second(error, {});
                            mDialogueCallbacks.erase(it);
                        }
                        return;
                    }

                    // Extract text and actions
                    std::string text = responseJson["text"];
                    std::vector<Action> actions;

                    if (responseJson.contains("actions") && responseJson["actions"].is_array())
                    {
                        for (const auto& actionJson : responseJson["actions"])
                        {
                            Action action;
                            std::string actionType = actionJson["type"];

                            // Convert action type string to enum
                            if (actionType == "EMOTE")
                                action.type = ActionType::Emote;
                            else if (actionType == "GIVE_ITEM")
                                action.type = ActionType::GiveItem;
                            else if (actionType == "TAKE_ITEM")
                                action.type = ActionType::TakeItem;
                            else if (actionType == "START_BARTER")
                                action.type = ActionType::StartBarter;
                            else if (actionType == "ATTACK")
                                action.type = ActionType::Attack;
                            else if (actionType == "END_CONVERSATION")
                                action.type = ActionType::EndConversation;
                            else
                                action.type = ActionType::None;

                            // Extract parameters
                            if (actionJson.contains("params") && actionJson["params"].is_object())
                            {
                                for (auto& [key, value] : actionJson["params"].items())
                                {
                                    if (value.is_string())
                                        action.params.params[key] = value.get<std::string>();
                                    else
                                        action.params.params[key] = value.dump();
                                }
                            }

                            actions.push_back(action);
                        }
                    }

                    // Call callback
                    std::lock_guard<std::mutex> lock(mMutex);
                    auto it = mDialogueCallbacks.find(requestId);
                    if (it != mDialogueCallbacks.end())
                    {
                        it->second(text, actions);
                        mDialogueCallbacks.erase(it);
                    }
                }
                catch (const std::exception& e)
                {
                    std::cerr << "Error parsing dialogue response: " << e.what() << std::endl;
                    std::lock_guard<std::mutex> lock(mMutex);
                    auto it = mDialogueCallbacks.find(requestId);
                    if (it != mDialogueCallbacks.end())
                    {
                        it->second("Error parsing response: " + std::string(e.what()), {});
                        mDialogueCallbacks.erase(it);
                    }
                }
            }});
        }

        // Notify processing thread
        mRequestCondition.notify_one();
    }

    void Client::sendEvent(
        const std::string& npcId,
        EventType eventType,
        const std::string& description,
        EventCallback callback)
    {
        if (!mConnected)
        {
            if (!connect())
            {
                callback(false);
                return;
            }
        }

        // Generate request ID
        std::string requestId = generateRequestId();

        // Convert event type to string
        std::string eventTypeStr;
        switch (eventType)
        {
            case EventType::PlayerJoinedFaction:
                eventTypeStr = "PLAYER_JOINED_FACTION";
                break;
            case EventType::PlayerLeftFaction:
                eventTypeStr = "PLAYER_LEFT_FACTION";
                break;
            case EventType::PlayerCompletedQuest:
                eventTypeStr = "PLAYER_COMPLETED_QUEST";
                break;
            case EventType::PlayerFailedQuest:
                eventTypeStr = "PLAYER_FAILED_QUEST";
                break;
            case EventType::PlayerPromotion:
                eventTypeStr = "PLAYER_PROMOTION";
                break;
            case EventType::PlayerDemotion:
                eventTypeStr = "PLAYER_DEMOTION";
                break;
            case EventType::PlayerGaveItem:
                eventTypeStr = "PLAYER_GAVE_ITEM";
                break;
            case EventType::PlayerTookItem:
                eventTypeStr = "PLAYER_TOOK_ITEM";
                break;
            case EventType::NPCAttacked:
                eventTypeStr = "NPC_ATTACKED";
                break;
            case EventType::NPCKilled:
                eventTypeStr = "NPC_KILLED";
                break;
            default:
                eventTypeStr = "UNKNOWN";
                break;
        }

        // Create JSON request
        json request;
        request["type"] = "event";
        request["requestId"] = requestId;
        request["npcId"] = npcId;
        request["eventType"] = eventTypeStr;
        request["description"] = description;

        // Convert to string
        std::string requestStr = request.dump();

        // Store callback
        {
            std::lock_guard<std::mutex> lock(mMutex);
            mEventCallbacks[requestId] = callback;
        }

        // Add to request queue
        {
            std::lock_guard<std::mutex> lock(mMutex);
            mRequestQueue.push({requestStr, [this, requestId](const std::string& response) {
                try
                {
                    // Parse response
                    json responseJson = json::parse(response);

                    // Check for error
                    if (responseJson.contains("error"))
                    {
                        std::cerr << "Error from AI server: " << responseJson["error"] << std::endl;
                        std::lock_guard<std::mutex> lock(mMutex);
                        auto it = mEventCallbacks.find(requestId);
                        if (it != mEventCallbacks.end())
                        {
                            it->second(false);
                            mEventCallbacks.erase(it);
                        }
                        return;
                    }

                    // Check status
                    bool success = responseJson.contains("status") && responseJson["status"] == "success";

                    // Call callback
                    std::lock_guard<std::mutex> lock(mMutex);
                    auto it = mEventCallbacks.find(requestId);
                    if (it != mEventCallbacks.end())
                    {
                        it->second(success);
                        mEventCallbacks.erase(it);
                    }
                }
                catch (const std::exception& e)
                {
                    std::cerr << "Error parsing event response: " << e.what() << std::endl;
                    std::lock_guard<std::mutex> lock(mMutex);
                    auto it = mEventCallbacks.find(requestId);
                    if (it != mEventCallbacks.end())
                    {
                        it->second(false);
                        mEventCallbacks.erase(it);
                    }
                }
            }});
        }

        // Notify processing thread
        mRequestCondition.notify_one();
    }

    void Client::runIoContext()
    {
        // Start processing queue
        std::thread processingThread(&Client::processQueue, this);

        // Create buffer for reading
        beast::flat_buffer buffer;

        // Read loop
        while (mRunning)
        {
            try
            {
                // Read a message
                mWebSocket->read(buffer);

                // Get the message as a string
                std::string response = beast::buffers_to_string(buffer.data());

                // Clear the buffer
                buffer.consume(buffer.size());

                // Handle the response
                handleResponse(response);
            }
            catch (const websocket::close_reason& reason)
            {
                // WebSocket closed
                std::cerr << "WebSocket closed: " << reason.reason << std::endl;
                mConnected = false;
                mRunning = false;
                break;
            }
            catch (const std::exception& e)
            {
                // Error reading from WebSocket
                std::cerr << "Error reading from WebSocket: " << e.what() << std::endl;
                mConnected = false;
                mRunning = false;
                break;
            }
        }

        // Wait for processing thread to finish
        if (processingThread.joinable())
            processingThread.join();
    }

    void Client::processQueue()
    {
        while (mRunning)
        {
            Request request;

            // Get a request from the queue
            {
                std::unique_lock<std::mutex> lock(mMutex);
                mRequestCondition.wait(lock, [this] { return !mRequestQueue.empty() || !mRunning; });

                if (!mRunning)
                    break;

                request = mRequestQueue.front();
                mRequestQueue.pop();
            }

            try
            {
                // Send the request
                mWebSocket->write(net::buffer(request.message));
            }
            catch (const std::exception& e)
            {
                std::cerr << "Error sending request: " << e.what() << std::endl;
                request.callback("Error sending request: " + std::string(e.what()));
            }
        }
    }

    void Client::handleResponse(const std::string& response)
    {
        try
        {
            // Parse response
            json responseJson = json::parse(response);

            // Check if response has a request ID
            if (responseJson.contains("requestId"))
            {
                std::string requestId = responseJson["requestId"];

                // Find callback
                std::function<void(const std::string&)> callback;
                {
                    std::lock_guard<std::mutex> lock(mMutex);
                    auto dialogueIt = mDialogueCallbacks.find(requestId);
                    if (dialogueIt != mDialogueCallbacks.end())
                    {
                        // Call the callback with the response
                        callback = [this, requestId, response](const std::string&) {
                            try
                            {
                                // Parse response
                                json responseJson = json::parse(response);

                                // Extract text and actions
                                std::string text = responseJson["text"];
                                std::vector<Action> actions;

                                if (responseJson.contains("actions") && responseJson["actions"].is_array())
                                {
                                    for (const auto& actionJson : responseJson["actions"])
                                    {
                                        Action action;
                                        std::string actionType = actionJson["type"];

                                        // Convert action type string to enum
                                        if (actionType == "EMOTE")
                                            action.type = ActionType::Emote;
                                        else if (actionType == "GIVE_ITEM")
                                            action.type = ActionType::GiveItem;
                                        else if (actionType == "TAKE_ITEM")
                                            action.type = ActionType::TakeItem;
                                        else if (actionType == "START_BARTER")
                                            action.type = ActionType::StartBarter;
                                        else if (actionType == "ATTACK")
                                            action.type = ActionType::Attack;
                                        else if (actionType == "END_CONVERSATION")
                                            action.type = ActionType::EndConversation;
                                        else
                                            action.type = ActionType::None;

                                        // Extract parameters
                                        if (actionJson.contains("params") && actionJson["params"].is_object())
                                        {
                                            for (auto& [key, value] : actionJson["params"].items())
                                            {
                                                if (value.is_string())
                                                    action.params.params[key] = value.get<std::string>();
                                                else
                                                    action.params.params[key] = value.dump();
                                            }
                                        }

                                        actions.push_back(action);
                                    }
                                }

                                // Call callback
                                std::lock_guard<std::mutex> lock(mMutex);
                                auto it = mDialogueCallbacks.find(requestId);
                                if (it != mDialogueCallbacks.end())
                                {
                                    it->second(text, actions);
                                    mDialogueCallbacks.erase(it);
                                }
                            }
                            catch (const std::exception& e)
                            {
                                std::cerr << "Error parsing dialogue response: " << e.what() << std::endl;
                                std::lock_guard<std::mutex> lock(mMutex);
                                auto it = mDialogueCallbacks.find(requestId);
                                if (it != mDialogueCallbacks.end())
                                {
                                    it->second("Error parsing response: " + std::string(e.what()), {});
                                    mDialogueCallbacks.erase(it);
                                }
                            }
                        };
                    }
                    else
                    {
                        auto eventIt = mEventCallbacks.find(requestId);
                        if (eventIt != mEventCallbacks.end())
                        {
                            // Call the callback with the response
                            callback = [this, requestId, response](const std::string&) {
                                try
                                {
                                    // Parse response
                                    json responseJson = json::parse(response);

                                    // Check for error
                                    if (responseJson.contains("error"))
                                    {
                                        std::cerr << "Error from AI server: " << responseJson["error"] << std::endl;
                                        std::lock_guard<std::mutex> lock(mMutex);
                                        auto it = mEventCallbacks.find(requestId);
                                        if (it != mEventCallbacks.end())
                                        {
                                            it->second(false);
                                            mEventCallbacks.erase(it);
                                        }
                                        return;
                                    }

                                    // Check status
                                    bool success = responseJson.contains("status") && responseJson["status"] == "success";

                                    // Call callback
                                    std::lock_guard<std::mutex> lock(mMutex);
                                    auto it = mEventCallbacks.find(requestId);
                                    if (it != mEventCallbacks.end())
                                    {
                                        it->second(success);
                                        mEventCallbacks.erase(it);
                                    }
                                }
                                catch (const std::exception& e)
                                {
                                    std::cerr << "Error parsing event response: " << e.what() << std::endl;
                                    std::lock_guard<std::mutex> lock(mMutex);
                                    auto it = mEventCallbacks.find(requestId);
                                    if (it != mEventCallbacks.end())
                                    {
                                        it->second(false);
                                        mEventCallbacks.erase(it);
                                    }
                                }
                            };
                        }
                    }
                }

                // Call the callback if found
                if (callback)
                    callback(response);
            }
        }
        catch (const std::exception& e)
        {
            std::cerr << "Error handling response: " << e.what() << std::endl;
        }
    }

    std::string Client::generateRequestId()
    {
        // Generate a random request ID
        static std::random_device rd;
        static std::mt19937 gen(rd());
        static std::uniform_int_distribution<> dis(0, 15);
        static const char* digits = "0123456789abcdef";

        std::stringstream ss;
        for (int i = 0; i < 32; ++i)
        {
            ss << digits[dis(gen)];
        }
        return ss.str();
    }
}
