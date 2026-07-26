/*
 * File: VOS/apps/terminal/shell/commands/cat.c
 *
 * Implements the cat command.
 */


#include "../include/command.h"
#include "../include/host_manager.h"

#include <stdlib.h>
#include <string.h>



static CommandResult cat_execute(
    int argc,
    char **argv
)
{
    CommandResult result;


    result.success = 1;
    result.exit_code = 0;
    result.error = NULL;
    result.output = NULL;



    if (argc < 2)
    {
        result.success = 0;
        result.error = "Usage: cat <file>";

        return result;
    }



    char *buffer = malloc(4096);


    if (buffer == NULL)
    {
        result.success = 0;
        result.error = "Memory allocation failed.";

        return result;
    }


    buffer[0] = '\0';



    host_manager_cat(
        argv[1],
        buffer,
        4096
    );

    result.output = buffer;


    return result;
}



Command cat_command =
{
    .name = "cat",
    .description = "Display file contents",
    .execute = cat_execute
};