/*
 * File: VOS/apps/terminal/shell/src/command_loader.c
 *
 * Registers built-in commands.
 */

#include <stdio.h>

#include "../include/command_loader.h"

#include "../include/command_registry.h"

#include "../include/command.h"


/*
 * Command defined in help.c
 */
extern Command help_command;
extern Command echo_command;
extern Command clear_command;
extern Command version_command;
extern Command about_command;
extern Command exit_command;
extern Command date_command;
extern Command time_command;
extern Command pwd_command;
extern Command ls_command;
extern Command cd_command;
extern Command mkdir_command;
extern Command touch_command;
extern Command cat_command;
extern Command write_command;
extern Command rm_command;
extern Command rmdir_command;
extern Command tree_command;
extern Command mv_command;
extern Command cp_command;

void load_commands(void)
{
    registry_register(&help_command);
    registry_register(&echo_command);
    registry_register(&clear_command);
    registry_register(&version_command);
    registry_register(&about_command);
    registry_register(&exit_command);
    registry_register(&date_command);
    registry_register(&time_command);
    registry_register(&pwd_command);
    registry_register(&ls_command);
    registry_register(&cd_command);
    registry_register(&mkdir_command);
    registry_register(&touch_command);
    registry_register(&cat_command);
    registry_register(&write_command);
    registry_register(&rm_command);
    registry_register(&rmdir_command);
    registry_register(&tree_command);
    registry_register(&mv_command);
    registry_register(&cp_command);
}