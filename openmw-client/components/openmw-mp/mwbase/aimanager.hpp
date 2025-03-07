#ifndef OPENMW_COMPONENTS_MWBASE_AIMANAGER_H
#define OPENMW_COMPONENTS_MWBASE_AIMANAGER_H

#include <string>
#include <map>
#include <functional>
#include <vector>

namespace MWBase
{
    /**
     * @brief Interface for the AI manager
     */
    class AIManager
    {
    public:
        /**
         * @brief Callback type for dialogue responses
         */
        using DialogueCallback = std::function<void(const std::string&, const std::vector<std::pair<std::string, std::map<std::string, std::string>>>&)>;

        /**
         * @brief Callback type for event responses
         */
        using EventCallback = std::function<void(bool)>;

        /**
         * @brief Virtual destructor
         */
        virtual ~AIManager() = default;

        /**
         * @brief Initialize the AI manager
         * 
         * @param host Server host
         * @param port Server port
         * @return true if initialization successful, false otherwise
         */
        virtual bool init(const std::string& host, unsigned short port) = 0;

        /**
         * @brief Shutdown the AI manager
         */
        virtual void shutdown() = 0;

        /**
         * @brief Check if the AI manager is initialized
         * 
         * @return true if initialized, false otherwise
         */
        virtual bool isInitialized() const = 0;

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
        virtual void sendDialogueRequest(
            const std::string& npcId,
            const std::string& npcName,
            const std::string& npcRace,
            const std::string& npcGender,
            const std::string& npcClass,
            const std::string& npcFaction,
            const std::string& playerMessage,
            const std::map<std::string, std::string>& gameState,
            DialogueCallback callback
        ) = 0;

        /**
         * @brief Send a player joined faction event to the AI server
         * 
         * @param npcId NPC ID
         * @param factionName Faction name
         * @param rank Rank in the faction
         * @param callback Callback function for the response
         */
        virtual void sendPlayerJoinedFactionEvent(
            const std::string& npcId,
            const std::string& factionName,
            const std::string& rank,
            EventCallback callback
        ) = 0;

        /**
         * @brief Send a player left faction event to the AI server
         * 
         * @param npcId NPC ID
         * @param factionName Faction name
         * @param callback Callback function for the response
         */
        virtual void sendPlayerLeftFactionEvent(
            const std::string& npcId,
            const std::string& factionName,
            EventCallback callback
        ) = 0;

        /**
         * @brief Send a player completed quest event to the AI server
         * 
         * @param npcId NPC ID
         * @param questName Quest name
         * @param callback Callback function for the response
         */
        virtual void sendPlayerCompletedQuestEvent(
            const std::string& npcId,
            const std::string& questName,
            EventCallback callback
        ) = 0;

        /**
         * @brief Send a player failed quest event to the AI server
         * 
         * @param npcId NPC ID
         * @param questName Quest name
         * @param callback Callback function for the response
         */
        virtual void sendPlayerFailedQuestEvent(
            const std::string& npcId,
            const std::string& questName,
            EventCallback callback
        ) = 0;

        /**
         * @brief Send a player promotion event to the AI server
         * 
         * @param npcId NPC ID
         * @param factionName Faction name
         * @param newRank New rank in the faction
         * @param callback Callback function for the response
         */
        virtual void sendPlayerPromotionEvent(
            const std::string& npcId,
            const std::string& factionName,
            const std::string& newRank,
            EventCallback callback
        ) = 0;

        /**
         * @brief Send a player demotion event to the AI server
         * 
         * @param npcId NPC ID
         * @param factionName Faction name
         * @param newRank New rank in the faction
         * @param callback Callback function for the response
         */
        virtual void sendPlayerDemotionEvent(
            const std::string& npcId,
            const std::string& factionName,
            const std::string& newRank,
            EventCallback callback
        ) = 0;

        /**
         * @brief Send a player gave item event to the AI server
         * 
         * @param npcId NPC ID
         * @param itemId Item ID
         * @param count Item count
         * @param callback Callback function for the response
         */
        virtual void sendPlayerGaveItemEvent(
            const std::string& npcId,
            const std::string& itemId,
            int count,
            EventCallback callback
        ) = 0;

        /**
         * @brief Send a player took item event to the AI server
         * 
         * @param npcId NPC ID
         * @param itemId Item ID
         * @param count Item count
         * @param callback Callback function for the response
         */
        virtual void sendPlayerTookItemEvent(
            const std::string& npcId,
            const std::string& itemId,
            int count,
            EventCallback callback
        ) = 0;

        /**
         * @brief Send an NPC attacked event to the AI server
         * 
         * @param npcId NPC ID
         * @param attackerId Attacker ID
         * @param callback Callback function for the response
         */
        virtual void sendNPCAttackedEvent(
            const std::string& npcId,
            const std::string& attackerId,
            EventCallback callback
        ) = 0;

        /**
         * @brief Send an NPC killed event to the AI server
         * 
         * @param npcId NPC ID
         * @param killerId Killer ID
         * @param callback Callback function for the response
         */
        virtual void sendNPCKilledEvent(
            const std::string& npcId,
            const std::string& killerId,
            EventCallback callback
        ) = 0;
    };
}

#endif // OPENMW_COMPONENTS_MWBASE_AIMANAGER_H
