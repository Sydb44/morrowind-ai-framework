#ifndef OPENMW_COMPONENTS_LUA_AI_H
#define OPENMW_COMPONENTS_LUA_AI_H

#include <sol/sol.hpp>

namespace MWBase
{
    class AIManager;
}

namespace LuaUtil
{
    /**
     * @brief Register AI functions with the Lua state
     * 
     * @param lua Lua state
     * @param aiManager AI manager
     */
    void registerAIFunctions(sol::state& lua, MWBase::AIManager* aiManager);
}

#endif // OPENMW_COMPONENTS_LUA_AI_H
