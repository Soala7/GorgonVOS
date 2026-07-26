/*
 * File: tree.c
 *
 * Implements the tree command.
 */

#include "../include/command.h"
#include "../include/host.h"

#include <string.h>


static CommandResult tree_execute(
    int argc,
    char **argv
)
{
    CommandResult result;

    static char buffer[4096];


    memset(
        buffer,
        0,
        sizeof(buffer)
    );


    host_tree(
        buffer,
        sizeof(buffer)
    );


    result.success = 1;
    result.exit_code = 0;
    result.output = buffer;
    result.error = NULL;


    return result;
}


Command tree_command =
{
    .name = "tree",
    .description = "Display filesystem tree",
    .execute = tree_execute
};