-- Morrowind AI Framework - NPC Dialogue Script
-- This script handles NPC dialogue using the AI system

-- Configuration
local config = {
    debug = true,  -- Enable debug output
    logLevel = "info",  -- Log level: debug, info, warning, error
}

-- Log function
local function log(level, message)
    if level == "debug" and not config.debug then
        return
    end
    
    local logLevels = {debug = 0, info = 1, warning = 2, error = 3}
    if logLevels[level] < logLevels[config.logLevel] then
        return
    end
    
    local prefix = "[AI] " .. level:upper() .. ": "
    core.log(prefix .. message)
end

-- NPC registry
local npcs = {}

-- Register an NPC with the AI system
local function registerNPC(npcId)
    if npcs[npcId] then
        log("info", "NPC already registered: " .. npcId)
        return
    end
    
    log("info", "Registering NPC: " .. npcId)
    npcs[npcId] = {
        id = npcId,
        conversations = {},
    }
end

-- Get current game state
local function getGameState()
    local player = tes3.player
    if not player then
        log("warning", "Player not found")
        return {}
    end
    
    local playerCell = player.cell
    local cellName = playerCell and playerCell.name or "Unknown"
    
    local gameState = {
        player_name = player.name,
        player_race = player.race.name,
        player_gender = player.female and "Female" or "Male",
        player_class = player.class.name,
        player_level = tostring(player.level),
        location = cellName,
        time_of_day = tes3.worldController.hour.value < 6 and "Night" or
                      tes3.worldController.hour.value < 12 and "Morning" or
                      tes3.worldController.hour.value < 18 and "Afternoon" or
                      "Evening",
        weather = tes3.worldController.weatherController.currentWeather.name,
    }
    
    -- Add faction information
    local factions = {}
    for faction, rank in pairs(player.factions) do
        factions[faction.name] = tostring(rank)
    end
    gameState.player_factions = table.concat(factions, ",")
    
    return gameState
end

-- Handle dialogue topic
local function handleDialogueTopic(npcId, topic)
    local npc = npcs[npcId]
    if not npc then
        log("warning", "NPC not registered: " .. npcId)
        return nil
    end
    
    log("debug", "Handling dialogue topic for NPC " .. npcId .. ": " .. topic)
    
    -- Get game state
    local gameState = getGameState()
    
    -- Send dialogue request to AI server
    local result = nil
    AI.sendDialogue(npcId, topic, gameState, function(text, actions)
        log("debug", "Received response from AI server: " .. text)
        
        -- Process actions
        local processedActions = {}
        for i, action in ipairs(actions) do
            local actionType = action[1]
            local params = action[2]
            
            log("debug", "Processing action: " .. actionType)
            
            if actionType == "EMOTE" then
                -- Handle emote action
                local emote = params.description or ""
                processedActions[#processedActions + 1] = {
                    type = "emote",
                    text = emote,
                }
            elseif actionType == "GIVE_ITEM" then
                -- Handle give item action
                local itemId = params.item_id or ""
                local count = tonumber(params.quantity) or 1
                
                -- Add item to player inventory
                tes3.addItem({
                    reference = tes3.player,
                    item = itemId,
                    count = count,
                    playSound = true,
                })
                
                processedActions[#processedActions + 1] = {
                    type = "give_item",
                    item = itemId,
                    count = count,
                }
            elseif actionType == "TAKE_ITEM" then
                -- Handle take item action
                local itemId = params.item_id or ""
                local count = tonumber(params.quantity) or 1
                
                -- Remove item from player inventory
                tes3.removeItem({
                    reference = tes3.player,
                    item = itemId,
                    count = count,
                    playSound = true,
                })
                
                processedActions[#processedActions + 1] = {
                    type = "take_item",
                    item = itemId,
                    count = count,
                }
            elseif actionType == "START_BARTER" then
                -- Handle start barter action
                processedActions[#processedActions + 1] = {
                    type = "start_barter",
                }
            elseif actionType == "ATTACK" then
                -- Handle attack action
                local reason = params.reason or ""
                
                processedActions[#processedActions + 1] = {
                    type = "attack",
                    reason = reason,
                }
            elseif actionType == "END_CONVERSATION" then
                -- Handle end conversation action
                local reason = params.reason or ""
                
                processedActions[#processedActions + 1] = {
                    type = "end_conversation",
                    reason = reason,
                }
            end
        end
        
        -- Store result
        result = {
            text = text,
            actions = processedActions,
        }
    end)
    
    return result
end

-- Register event handlers
local function registerEventHandlers()
    -- Register script for NPCs with the AIDialogue script
    local function onCellChanged(e)
        log("debug", "Cell changed: " .. (e.cell.name or "unnamed"))
        
        -- Find NPCs with AIDialogue script
        for _, ref in pairs(e.cell.actors) do
            if ref.object.script and ref.object.script.name == "AIDialogue" then
                local npcId = ref.object.script:getVariables()["NPCId"] or ref.object.id
                registerNPC(npcId)
            end
        end
    end
    
    -- Register dialogue handler
    local function onDialogue(e)
        local reference = e.reference
        if not reference or not reference.object.script or reference.object.script.name ~= "AIDialogue" then
            return
        end
        
        local npcId = reference.object.script:getVariables()["NPCId"] or reference.object.id
        local topic = e.topic
        
        log("debug", "Dialogue event for NPC " .. npcId .. ", topic: " .. topic)
        
        local result = handleDialogueTopic(npcId, topic)
        if result then
            e.text = result.text
            
            -- Process actions
            for _, action in ipairs(result.actions) do
                if action.type == "start_barter" then
                    tes3.startBarter(reference)
                elseif action.type == "attack" then
                    reference.mobile:startCombat(tes3.player)
                elseif action.type == "end_conversation" then
                    tes3.player:endConversation()
                end
            end
            
            e.block = true
        end
    end
    
    -- Register event handlers
    event.register("cellChanged", onCellChanged)
    event.register("dialogue topic", onDialogue)
    
    -- Initial cell scan
    if tes3.player and tes3.player.cell then
        onCellChanged({cell = tes3.player.cell})
    end
}

-- Initialize
local function initialize()
    log("info", "Initializing AI NPC Dialogue system")
    registerEventHandlers()
end

-- Register initialization
event.register("initialized", initialize)

-- Return public API
return {
    registerNPC = registerNPC,
    handleDialogueTopic = handleDialogueTopic,
}
