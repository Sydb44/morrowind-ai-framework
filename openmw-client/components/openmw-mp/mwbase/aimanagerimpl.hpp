#ifndef OPENMW_COMPONENTS_MWBASE_AIMANAGERIMPL_H
#define OPENMW_COMPONENTS_MWBASE_AIMANAGERIMPL_H

#include "aimanager.hpp"
#include <memory>

namespace AI
{
    class Client;
}

namespace MWBase
{
    /**
     * @brief Implementation of the AI manager
     */
    class AIManagerImpl : public AIManager
    {
    public:
        /**
         * @brief Constructor
         */
        AIManagerImpl();

        /**
         * @brief Destructor
         */
        ~AIManagerImpl() override;

        /**
         * @brief Initialize the AI manager
         * 
         * @param host Server host
         * @param port Server port
         * @return true if initialization successful, false otherwise
         */
        bool init(const std::string& host, unsigned short port) override;

        /**
         * @brief Shutdown the AI manager
         */
        void shutdown() override;

        /**
         * @brief Check if the AI manager is initialized
         * 
         * @return true if initialized, false otherwise
         */
        bool isInitialized() const override;

        /**
         * @brief Send a dialogue request to the AI server
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
        ) override;

        /**
         * @brief Send a player joined faction event to the AI server
         * 
         * @param npcId NPC ID
         * @param factionName Faction name
         * @param rank Rank in the faction
         * @param callback Callback function for the response
         */
        void sendPlayerJoinedFactionEvent(
            const std::string& npcId,
            const std::string& factionName,
            const std::string& rank,
            EventCallback callback
        ) override;

        /**
         * @brief Send a player left faction event to the AI server
         * 
         * @param npcId NPC ID
         * @param factionName Faction name
         * @param callback Callback function for the response
         */
        void sendPlayerLeftFactionEvent(
            const std::string& npcId,
            const std::string& factionName,
            EventCallback callback
        ) override;

        /**
         * @brief Send a player completed quest event to the AI server
         * 
         * @param npcId NPC ID
         * @param questName Quest name
         * @param callback Callback function for the response
         */
        void sendPlayerCompletedQuestEvent(
            const std::string& npcId,
            const std::string& questName,
            EventCallback callback
        ) override;

        /**
         * @brief Send a player failed quest event to the AI server
         * 
         * @param npcId NPC ID
         * @param questName Quest name
         * @param callback Callback function for the response
         */
        void sendPlayerFailedQuestEvent(
            const std::string& npcId,
            const std::string& questName,
            EventCallback callback
        ) override;

        /**
         * @brief Send a player promotion event to the AI server
         * 
         * @param npcId NPC ID
         * @param factionName Faction name
         * @param newRank New rank in the faction
         * @param callback Callback function for the response
         */
        void sendPlayerPromotionEvent(
            const std::string& npcId,
            const std::string& factionName,
            const std::string& newRank,
            EventCallback callback
        ) override;

        /**
         * @brief Send a player demotion event to the AI server
         * 
         * @param npcId NPC ID
         * @param factionName Faction name
         * @param newRank New rank in the faction
         * @param callback Callback function for the response
         */
        void sendPlayerDemotionEvent(
            const std::string& npcId,
            const std::string& factionName,
            const std::string& newRank,
            EventCallback callback
        ) override;

        /**
         * @brief Send a player gave item event to the AI server
         * 
         * @param npcId NPC ID
         * @param itemId Item ID
         * @param count Item count
         * @param callback Callback function for the response
         */
        void sendPlayerGaveItemEvent(
            const std::string& npcId,
            const std::string& itemId,
            int count,
            EventCallback callback
        ) override;

        /**
         * @brief Send a player took item event to the AI server
         * 
         * @param npcId NPC ID
         * @param itemId Item ID
         * @param count Item count
         * @param callback Callback function for the response
         */
        void sendPlayerTookItemEvent(
            const std::string& npcId,
            const std::string& itemId,
            int count,
            EventCallback callback
        ) override;

        /**
         * @brief Send an NPC attacked event to the AI server
         * 
         * @param npcId NPC ID
         * @param attackerId Attacker ID
         * @param callback Callback function for the response
         */
        void sendNPCAttackedEvent(
            const std::string& npcId,
            const std::string& attackerId,
            EventCallback callback
        ) override;

        /**
         * @brief Send an NPC killed event to the AI server
         * 
         * @param npcId NPC ID
         * @param killerId Killer ID
         * @param callback Callback function for the response
         */
        void sendNPCKilledEvent(
            const std::string& npcId,
            const std::string& killerId,
            EventCallback callback
        ) override;

    private:
        /**
         * @brief Convert AI client actions to AI manager actions
         * 
         * @param clientActions Client actions
         * @return AI manager actions
         */
        std::vector<std::pair<std::string, std::map<std::string, std::string>>> convertActions(
            const std::vector<std::pair<std::string, std::map<std::string, std::string>>>& clientActions
        );

        // AI client
        std::unique_ptr<AI::Client> mClient;

        // Initialization state
        bool mInitialized;
    };
}

#endif // OPENMW_COMPONENTS_MWBASE_AIMANAGERIMPL_H
