/*
 * File: rm_command.c
 *
 * Implements the rm command.
 */

#include "../include/command.h"
#include "../include/host.h"

#include <stdio.h>


static CommandResult rm_execute(
    int argc,
    char **argv
)
{
    CommandResult result;


    result.success = 1;
    result.exit_code = 0;
    result.output = "File deleted.";
    result.error = NULL;


    if (argc < 2)
    {
        result.success = 0;
        result.error = "Usage: rm <file>";

        return result;
    }


    if (!host_rm(argv[1]))
    {
        result.success = 0;
        result.error = "Failed to delete file.";

        return result;
    }


    return result;
}


Command rm_command =
{
    .name = "rm",
    .description = "Delete a file",
    .execute = rm_execute
};