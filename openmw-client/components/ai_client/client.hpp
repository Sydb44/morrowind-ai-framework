#ifndef OPENMW_COMPONENTS_AI_CLIENT_CLIENT_H
#define OPENMW_COMPONENTS_AI_CLIENT_CLIENT_H

#include <string>
#include <vector>
#include <map>
#include <functional>
#include <memory>
#include <mutex>
#include <thread>
#include <condition_variable>
#include <queue>
#include <atomic>

#include <boost/beast/core.hpp>
#include <boost/beast/websocket.hpp>
#include <boost/asio/ip/tcp.hpp>

namespace AI
{
    /**
     * @brief Enum for action types that can be performed by NPCs
     */
    enum class ActionType
    {
        None,
        Emote,
        GiveItem,
        TakeItem,
        StartBarter,
        Attack,
        EndConversation
    };

    /**
     * @brief Struct for action parameters
     */
    struct ActionParams
    {
        std::map<std::string, std::string> params;
    };

    /**
     * @brief Struct for an NPC action
     */
    struct Action
    {
        ActionType type;
        ActionParams params;
    };

    /**
     * @brief Enum for event types that can be sent to the AI server
     */
    enum class EventType
    {
        None,
        PlayerJoinedFaction,
        PlayerLeftFaction,
        PlayerCompletedQuest,
        PlayerFailedQuest,
        PlayerPromotion,
        PlayerDemotion,
        PlayerGaveItem,
        PlayerTookItem,
        NPCAttacked,
        NPCKilled
    };

    /**
     * @brief Callback type for dialogue responses
     */
    using DialogueCallback = std::function<void(const std::string&, const std::vector<Action>&)>;

    /**
     * @brief Callback type for event responses
     */
    using EventCallback = std::function<void(bool)>;

    /**
     * @brief Class for WebSocket client to communicate with the AI server
     */
    class Client
    {
    public:
        /**
         * @brief Constructor
         * 
         * @param host Server host
         * @param port Server port
         */
        Client(const std::string& host, unsigned short port);

        /**
         * @brief Destructor
         */
        ~Client();

        /**
         * @brief Connect to the server
         * 
         * @return true if connection successful, false otherwise
         */
        bool connect();

        /**
         * @brief Disconnect from the server
         */
        void disconnect();

        /**
         * @brief Check if connected to the server
         * 
         * @return true if connected, false otherwise
         */
        bool isConnected() const;

        /**
         * @brief Send a dialogue request to the server
         * 
         * @param npcId NPC ID
         * @param npcName NPC name
         * @param npcRace NPC race
         * @param npcGender NPC gender
         * @param npcClass NPC class
         * @param npcFaction NPC faction
         * @param playerMessage Player's message
         * @param gameState Game state information
         * @param callback Callback function for the response
         */
        void sendDialogueRequest(
            const std::string& npcId,
            const std::string& npcName,
            const std::string& npcRace,
            const std::string& npcGender,
            const std::string& npcClass,
            const std::string& npcFaction,
            const std::string& playerMessage,
            const std::map<std::string, std::string>& gameState,
            DialogueCallback callback
        );

        /**
         * @brief Send an event to the server
         * 
         * @param npcId NPC ID
         * @param eventType Event type
         * @param description Event description
         * @param callback Callback function for the response
         */
        void sendEvent(
            const std::string& npcId,
            EventType eventType,
            const std::string& description,
            EventCallback callback
        );

    private:
        // Server information
        std::string mHost;
        unsigned short mPort;
        
        // Connection state
        std::atomic<bool> mConnected;
        std::atomic<bool> mRunning;
        
        // Boost.Beast WebSocket
        boost::asio::io_context mIoContext;
        std::unique_ptr<boost::asio::ip::tcp::resolver> mResolver;
        std::unique_ptr<boost::beast::websocket::stream<boost::asio::ip::tcp::socket>> mWebSocket;
        
        // Thread for IO operations
        std::thread mIoThread;
        
        // Mutex for thread safety
        mutable std::mutex mMutex;
        
        // Request queue
        struct Request
        {
            std::string message;
            std::function<void(const std::string&)> callback;
        };
        std::queue<Request> mRequestQueue;
        std::condition_variable mRequestCondition;
        
        // Callbacks
        std::map<std::string, DialogueCallback> mDialogueCallbacks;
        std::map<std::string, EventCallback> mEventCallbacks;
        
        // Internal methods
        void runIoContext();
        void processQueue();
        void handleResponse(const std::string& response);
        std::string generateRequestId();
    };
}

#endif // OPENMW_COMPONENTS_AI_CLIENT_CLIENT_H
