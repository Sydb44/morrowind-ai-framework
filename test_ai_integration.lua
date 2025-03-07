-- Morrowind AI Framework - Integration Test Script
-- This script tests the AI integration by creating a test NPC and initiating dialogue

-- Print function for debugging
local function print(text)
    mwse.log("[AI Test] " .. text)
end

-- Create a test NPC
local function createTestNPC()
    print("Creating test NPC...")
    
    -- Get player position
    local player = tes3.player
    local playerPos = player.position
    local playerCell = player.cell
    
    -- Create NPC slightly in front of player
    local angle = math.rad(player.orientation.z)
    local distance = 100 -- 100 units in front
    local x = playerPos.x + distance * math.sin(angle)
    local y = playerPos.y + distance * math.cos(angle)
    local z = playerPos.z
    
    -- Create NPC reference
    local npc = tes3.createReference({
        object = "example_npc_test",
        position = tes3vector3.new(x, y, z),
        orientation = tes3vector3.new(0, 0, -angle),
        cell = playerCell
    })
    
    if npc then
        print("Test NPC created successfully")
        return npc
    else
        print("Failed to create test NPC")
        return nil
    end
end

-- Add AI dialogue script to NPC
local function addAIDialogueScript(npc)
    print("Adding AI dialogue script to NPC...")
    
    -- Create script
    local script = [[
Begin AIDialogue
    NPCId "example_npc"
End
]]
    
    -- Attach script to NPC
    tes3.setScript({
        reference = npc,
        script = script
    })
    
    print("AI dialogue script added")
end

-- Initiate dialogue with NPC
local function initiateDialogue(npc)
    print("Initiating dialogue with test NPC...")
    
    -- Activate NPC to start dialogue
    tes3.activate({
        activator = tes3.player,
        target = npc
    })
    
    print("Dialogue initiated")
end

-- Main test function
local function testAIIntegration()
    print("Starting AI integration test...")
    
    -- Check if AI manager is initialized
    if not tes3.aiManager or not tes3.aiManager.isInitialized() then
        print("ERROR: AI Manager not initialized. Integration may have failed.")
        return false
    end
    
    print("AI Manager is initialized")
    
    -- Create test NPC
    local npc = createTestNPC()
    if not npc then
        return false
    end
    
    -- Add AI dialogue script
    addAIDialogueScript(npc)
    
    -- Initiate dialogue
    initiateDialogue(npc)
    
    print("AI integration test completed")
    return true
end

-- Run the test
local success = testAIIntegration()
if success then
    tes3.messageBox("AI integration test completed successfully")
else
    tes3.messageBox("AI integration test failed. Check logs for details.")
end
