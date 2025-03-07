#include "aimanagerimpl.hpp"
#include "components/ai_client/client.hpp"

#include <iostream>
#include <sstream>

namespace MWBase
{
    AIManagerImpl::AIManagerImpl()
        : mInitialized(false)
    {
    }

    AIManagerImpl::~AIManagerImpl()
    {
        shutdown();
    }

    bool AIManagerImpl::init(const std::string& host, unsigned short port)
    {
        if (mInitialized)
            return true;

        try
        {
            // Create AI client
            mClient = std::make_unique<AI::Client>(host, port);

            // Connect to server
            if (!mClient->connect())
            {
                std::cerr << "Failed to connect to AI server at " << host << ":" << port << std::endl;
                return false;
            }

            mInitialized = true;
            return true;
        }
        catch (const std::exception& e)
        {
            std::cerr << "Error initializing AI manager: " << e.what() << std::endl;
            return false;
        }
    }

    void AIManagerImpl::shutdown()
    {
        if (!mInitialized)
            return;

        try
        {
            // Disconnect from server
            if (mClient)
                mClient->disconnect();

            // Reset client
            mClient.reset();

            mInitialized = false;
        }
        catch (const std::exception& e)
        {
            std::cerr << "Error shutting down AI manager: " << e.what() << std::endl;
        }
    }

    bool AIManagerImpl::isInitialized() const
    {
        return mInitialized;
    }

    void AIManagerImpl::sendDialogueRequest(
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
        if (!mInitialized)
        {
            callback("Error: AI manager not initialized", {});
            return;
        }

        // Send dialogue request to AI client
        mClient->sendDialogueRequest(
            npcId,
            npcName,
            npcRace,
            npcGender,
            npcClass,
            npcFaction,
            playerMessage,
            gameState,
            [callback](const std::string& text, const std::vector<AI::Action>& actions) {
                // Convert actions to the format expected by the callback
                std::vector<std::pair<std::string, std::map<std::string, std::string>>> convertedActions;
                for (const auto& action : actions)
                {
                    std::string actionType;
                    switch (action.type)
                    {
                        case AI::ActionType::Emote:
                            actionType = "EMOTE";
                            break;
                        case AI::ActionType::GiveItem:
                            actionType = "GIVE_ITEM";
                            break;
                        case AI::ActionType::TakeItem:
                            actionType = "TAKE_ITEM";
                            break;
                        case AI::ActionType::StartBarter:
                            actionType = "START_BARTER";
                            break;
                        case AI::ActionType::Attack:
                            actionType = "ATTACK";
                            break;
                        case AI::ActionType::EndConversation:
                            actionType = "END_CONVERSATION";
                            break;
                        default:
                            actionType = "UNKNOWN";
                            break;
                    }
                    convertedActions.emplace_back(actionType, action.params.params);
                }
                callback(text, convertedActions);
            }
        );
    }

    void AIManagerImpl::sendPlayerJoinedFactionEvent(
        const std::string& npcId,
        const std::string& factionName,
        const std::string& rank,
        EventCallback callback)
    {
        if (!mInitialized)
        {
            callback(false);
            return;
        }

        // Create description
        std::ostringstream description;
        description << "The player has joined " << factionName << " and is now a " << rank << ".";

        // Send event to AI client
        mClient->sendEvent(
            npcId,
            AI::EventType::PlayerJoinedFaction,
            description.str(),
            callback
        );
    }

    void AIManagerImpl::sendPlayerLeftFactionEvent(
        const std::string& npcId,
        const std::string& factionName,
        EventCallback callback)
    {
        if (!mInitialized)
        {
            callback(false);
            return;
        }

        // Create description
        std::ostringstream description;
        description << "The player has left " << factionName << ".";

        // Send event to AI client
        mClient->sendEvent(
            npcId,
            AI::EventType::PlayerLeftFaction,
            description.str(),
            callback
        );
    }

    void AIManagerImpl::sendPlayerCompletedQuestEvent(
        const std::string& npcId,
        const std::string& questName,
        EventCallback callback)
    {
        if (!mInitialized)
        {
            callback(false);
            return;
        }

        // Create description
        std::ostringstream description;
        description << "The player has completed the quest: " << questName << ".";

        // Send event to AI client
        mClient->sendEvent(
            npcId,
            AI::EventType::PlayerCompletedQuest,
            description.str(),
            callback
        );
    }

    void AIManagerImpl::sendPlayerFailedQuestEvent(
        const std::string& npcId,
        const std::string& questName,
        EventCallback callback)
    {
        if (!mInitialized)
        {
            callback(false);
            return;
        }

        // Create description
        std::ostringstream description;
        description << "The player has failed the quest: " << questName << ".";

        // Send event to AI client
        mClient->sendEvent(
            npcId,
            AI::EventType::PlayerFailedQuest,
            description.str(),
            callback
        );
    }

    void AIManagerImpl::sendPlayerPromotionEvent(
        const std::string& npcId,
        const std::string& factionName,
        const std::string& newRank,
        EventCallback callback)
    {
        if (!mInitialized)
        {
            callback(false);
            return;
        }

        // Create description
        std::ostringstream description;
        description << "The player has been promoted to " << newRank << " in " << factionName << ".";

        // Send event to AI client
        mClient->sendEvent(
            npcId,
            AI::EventType::PlayerPromotion,
            description.str(),
            callback
        );
    }

    void AIManagerImpl::sendPlayerDemotionEvent(
        const std::string& npcId,
        const std::string& factionName,
        const std::string& newRank,
        EventCallback callback)
    {
        if (!mInitialized)
        {
            callback(false);
            return;
        }

        // Create description
        std::ostringstream description;
        description << "The player has been demoted to " << newRank << " in " << factionName << ".";

        // Send event to AI client
        mClient->sendEvent(
            npcId,
            AI::EventType::PlayerDemotion,
            description.str(),
            callback
        );
    }

    void AIManagerImpl::sendPlayerGaveItemEvent(
        const std::string& npcId,
        const std::string& itemId,
        int count,
        EventCallback callback)
    {
        if (!mInitialized)
        {
            callback(false);
            return;
        }

        // Create description
        std::ostringstream description;
        description << "The player has given " << count << " " << itemId << " to the NPC.";

        // Send event to AI client
        mClient->sendEvent(
            npcId,
            AI::EventType::PlayerGaveItem,
            description.str(),
            callback
        );
    }

    void AIManagerImpl::sendPlayerTookItemEvent(
        const std::string& npcId,
        const std::string& itemId,
        int count,
        EventCallback callback)
    {
        if (!mInitialized)
        {
            callback(false);
            return;
        }

        // Create description
        std::ostringstream description;
        description << "The player has taken " << count << " " << itemId << " from the NPC.";

        // Send event to AI client
        mClient->sendEvent(
            npcId,
            AI::EventType::PlayerTookItem,
            description.str(),
            callback
        );
    }

    void AIManagerImpl::sendNPCAttackedEvent(
        const std::string& npcId,
        const std::string& attackerId,
        EventCallback callback)
    {
        if (!mInitialized)
        {
            callback(false);
            return;
        }

        // Create description
        std::ostringstream description;
        description << "The NPC has been attacked by " << attackerId << ".";

        // Send event to AI client
        mClient->sendEvent(
            npcId,
            AI::EventType::NPCAttacked,
            description.str(),
            callback
        );
    }

    void AIManagerImpl::sendNPCKilledEvent(
        const std::string& npcId,
        const std::string& killerId,
        EventCallback callback)
    {
        if (!mInitialized)
        {
            callback(false);
            return;
        }

        // Create description
        std::ostringstream description;
        description << "The NPC has been killed by " << killerId << ".";

        // Send event to AI client
        mClient->sendEvent(
            npcId,
            AI::EventType::NPCKilled,
            description.str(),
            callback
        );
    }

    std::vector<std::pair<std::string, std::map<std::string, std::string>>> AIManagerImpl::convertActions(
        const std::vector<std::pair<std::string, std::map<std::string, std::string>>>& clientActions)
    {
        // This function is not used in the current implementation
        return clientActions;
    }
}
