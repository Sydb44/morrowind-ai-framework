#include "ai.hpp"
#include "components/openmw-mp/mwbase/aimanager.hpp"

#include <iostream>
#include <map>
#include <string>
#include <vector>

namespace LuaUtil
{
    void registerAIFunctions(sol::state& lua, MWBase::AIManager* aiManager)
    {
        // Create AI table
        auto ai = lua.create_named_table("AI");

        // Register AI functions
        ai.set_function("sendDialogue", [aiManager](
            const std::string& npcId,
            const std::string& playerMessage,
            sol::optional<sol::table> gameStateTable,
            sol::protected_function callback) -> void
        {
            if (!aiManager)
            {
                std::cerr << "Error: AI manager not initialized" << std::endl;
                return;
            }

            // Get NPC information from the NPC ID
            // In a real implementation, this would be retrieved from the game
            std::string npcName = "Unknown NPC";
            std::string npcRace = "Dunmer";
            std::string npcGender = "Male";
            std::string npcClass = "Warrior";
            std::string npcFaction = "None";

            // Convert game state table to map
            std::map<std::string, std::string> gameState;
            if (gameStateTable)
            {
                for (const auto& pair : gameStateTable.value())
                {
                    if (pair.second.is<std::string>())
                        gameState[pair.first.as<std::string>()] = pair.second.as<std::string>();
                }
            }

            // Send dialogue request
            aiManager->sendDialogueRequest(
                npcId,
                npcName,
                npcRace,
                npcGender,
                npcClass,
                npcFaction,
                playerMessage,
                gameState,
                [callback](const std::string& text, const std::vector<std::pair<std::string, std::map<std::string, std::string>>>& actions) {
                    // Call Lua callback with response
                    if (callback)
                    {
                        sol::protected_function_result result = callback(text, actions);
                        if (!result.valid())
                        {
                            sol::error err = result;
                            std::cerr << "Error in AI dialogue callback: " << err.what() << std::endl;
                        }
                    }
                }
            );
        });

        // Register event functions
        ai.set_function("sendPlayerJoinedFactionEvent", [aiManager](
            const std::string& npcId,
            const std::string& factionName,
            const std::string& rank,
            sol::optional<sol::protected_function> callback) -> void
        {
            if (!aiManager)
            {
                std::cerr << "Error: AI manager not initialized" << std::endl;
                return;
            }

            // Send event
            aiManager->sendPlayerJoinedFactionEvent(
                npcId,
                factionName,
                rank,
                [callback](bool success) {
                    // Call Lua callback with response
                    if (callback && callback.value())
                    {
                        sol::protected_function_result result = callback.value()(success);
                        if (!result.valid())
                        {
                            sol::error err = result;
                            std::cerr << "Error in AI event callback: " << err.what() << std::endl;
                        }
                    }
                }
            );
        });

        ai.set_function("sendPlayerLeftFactionEvent", [aiManager](
            const std::string& npcId,
            const std::string& factionName,
            sol::optional<sol::protected_function> callback) -> void
        {
            if (!aiManager)
            {
                std::cerr << "Error: AI manager not initialized" << std::endl;
                return;
            }

            // Send event
            aiManager->sendPlayerLeftFactionEvent(
                npcId,
                factionName,
                [callback](bool success) {
                    // Call Lua callback with response
                    if (callback && callback.value())
                    {
                        sol::protected_function_result result = callback.value()(success);
                        if (!result.valid())
                        {
                            sol::error err = result;
                            std::cerr << "Error in AI event callback: " << err.what() << std::endl;
                        }
                    }
                }
            );
        });

        ai.set_function("sendPlayerCompletedQuestEvent", [aiManager](
            const std::string& npcId,
            const std::string& questName,
            sol::optional<sol::protected_function> callback) -> void
        {
            if (!aiManager)
            {
                std::cerr << "Error: AI manager not initialized" << std::endl;
                return;
            }

            // Send event
            aiManager->sendPlayerCompletedQuestEvent(
                npcId,
                questName,
                [callback](bool success) {
                    // Call Lua callback with response
                    if (callback && callback.value())
                    {
                        sol::protected_function_result result = callback.value()(success);
                        if (!result.valid())
                        {
                            sol::error err = result;
                            std::cerr << "Error in AI event callback: " << err.what() << std::endl;
                        }
                    }
                }
            );
        });

        ai.set_function("sendPlayerFailedQuestEvent", [aiManager](
            const std::string& npcId,
            const std::string& questName,
            sol::optional<sol::protected_function> callback) -> void
        {
            if (!aiManager)
            {
                std::cerr << "Error: AI manager not initialized" << std::endl;
                return;
            }

            // Send event
            aiManager->sendPlayerFailedQuestEvent(
                npcId,
                questName,
                [callback](bool success) {
                    // Call Lua callback with response
                    if (callback && callback.value())
                    {
                        sol::protected_function_result result = callback.value()(success);
                        if (!result.valid())
                        {
                            sol::error err = result;
                            std::cerr << "Error in AI event callback: " << err.what() << std::endl;
                        }
                    }
                }
            );
        });

        ai.set_function("sendPlayerPromotionEvent", [aiManager](
            const std::string& npcId,
            const std::string& factionName,
            const std::string& newRank,
            sol::optional<sol::protected_function> callback) -> void
        {
            if (!aiManager)
            {
                std::cerr << "Error: AI manager not initialized" << std::endl;
                return;
            }

            // Send event
            aiManager->sendPlayerPromotionEvent(
                npcId,
                factionName,
                newRank,
                [callback](bool success) {
                    // Call Lua callback with response
                    if (callback && callback.value())
                    {
                        sol::protected_function_result result = callback.value()(success);
                        if (!result.valid())
                        {
                            sol::error err = result;
                            std::cerr << "Error in AI event callback: " << err.what() << std::endl;
                        }
                    }
                }
            );
        });

        ai.set_function("sendPlayerDemotionEvent", [aiManager](
            const std::string& npcId,
            const std::string& factionName,
            const std::string& newRank,
            sol::optional<sol::protected_function> callback) -> void
        {
            if (!aiManager)
            {
                std::cerr << "Error: AI manager not initialized" << std::endl;
                return;
            }

            // Send event
            aiManager->sendPlayerDemotionEvent(
                npcId,
                factionName,
                newRank,
                [callback](bool success) {
                    // Call Lua callback with response
                    if (callback && callback.value())
                    {
                        sol::protected_function_result result = callback.value()(success);
                        if (!result.valid())
                        {
                            sol::error err = result;
                            std::cerr << "Error in AI event callback: " << err.what() << std::endl;
                        }
                    }
                }
            );
        });

        ai.set_function("sendPlayerGaveItemEvent", [aiManager](
            const std::string& npcId,
            const std::string& itemId,
            int count,
            sol::optional<sol::protected_function> callback) -> void
        {
            if (!aiManager)
            {
                std::cerr << "Error: AI manager not initialized" << std::endl;
                return;
            }

            // Send event
            aiManager->sendPlayerGaveItemEvent(
                npcId,
                itemId,
                count,
                [callback](bool success) {
                    // Call Lua callback with response
                    if (callback && callback.value())
                    {
                        sol::protected_function_result result = callback.value()(success);
                        if (!result.valid())
                        {
                            sol::error err = result;
                            std::cerr << "Error in AI event callback: " << err.what() << std::endl;
                        }
                    }
                }
            );
        });

        ai.set_function("sendPlayerTookItemEvent", [aiManager](
            const std::string& npcId,
            const std::string& itemId,
            int count,
            sol::optional<sol::protected_function> callback) -> void
        {
            if (!aiManager)
            {
                std::cerr << "Error: AI manager not initialized" << std::endl;
                return;
            }

            // Send event
            aiManager->sendPlayerTookItemEvent(
                npcId,
                itemId,
                count,
                [callback](bool success) {
                    // Call Lua callback with response
                    if (callback && callback.value())
                    {
                        sol::protected_function_result result = callback.value()(success);
                        if (!result.valid())
                        {
                            sol::error err = result;
                            std::cerr << "Error in AI event callback: " << err.what() << std::endl;
                        }
                    }
                }
            );
        });

        ai.set_function("sendNPCAttackedEvent", [aiManager](
            const std::string& npcId,
            const std::string& attackerId,
            sol::optional<sol::protected_function> callback) -> void
        {
            if (!aiManager)
            {
                std::cerr << "Error: AI manager not initialized" << std::endl;
                return;
            }

            // Send event
            aiManager->sendNPCAttackedEvent(
                npcId,
                attackerId,
                [callback](bool success) {
                    // Call Lua callback with response
                    if (callback && callback.value())
                    {
                        sol::protected_function_result result = callback.value()(success);
                        if (!result.valid())
                        {
                            sol::error err = result;
                            std::cerr << "Error in AI event callback: " << err.what() << std::endl;
                        }
                    }
                }
            );
        });

        ai.set_function("sendNPCKilledEvent", [aiManager](
            const std::string& npcId,
            const std::string& killerId,
            sol::optional<sol::protected_function> callback) -> void
        {
            if (!aiManager)
            {
                std::cerr << "Error: AI manager not initialized" << std::endl;
                return;
            }

            // Send event
            aiManager->sendNPCKilledEvent(
                npcId,
                killerId,
                [callback](bool success) {
                    // Call Lua callback with response
                    if (callback && callback.value())
                    {
                        sol::protected_function_result result = callback.value()(success);
                        if (!result.valid())
                        {
                            sol::error err = result;
                            std::cerr << "Error in AI event callback: " << err.what() << std::endl;
                        }
                    }
                }
            );
        });
    }
}
