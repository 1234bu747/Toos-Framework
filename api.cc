#ifndef __cplusplus
#define _GNU_SOURCE
#endif
#include <unistd.h>
#include <dirent.h>
#include <sys/types.h> // for opendir(), readdir(), closedir() 
#include <sys/stat.h> //for stat()
#include <iostream>
#include <cstdlib>
#include <cstring>
#include <cstdarg> 
#define PROC_DIRECTORY "/proc/"
#define CASE_SENSITIVE 1
#define CASE_INSENSITIVE 0
#define EXACT_MATCH 1
#define INEXACT_MATCH 0
//是不是数字
int IsNumeric(const char *ccharptr_CharacterList)
{
    for (; *ccharptr_CharacterList; ccharptr_CharacterList++)
        if (*ccharptr_CharacterList < '0' || *ccharptr_CharacterList > '9')
            return 0; // false
    return 1;         // true
}

long strcmp_Wrapper(const char *s1, const char *s2, int intCaseSensitive)
{
    if (intCaseSensitive)
        return !strcmp(s1, s2);
    else
        return !strcasecmp(s1, s2);
}

long strstr_Wrapper(const char *haystack, const char *needle, int intCaseSensitive)
{
    if (intCaseSensitive)
        return (long)strstr(haystack, needle);
    else
        return (long)strcasestr(haystack, needle);
}
void GetPIDbyName_v2(pid_t *pid_ProcessIdentifier, const char *cchrptr_ProcessName, int intCaseSensitiveness, int intExactMatch)
{
    char chrarry_CommandLinePath[1024*8] = {'\0'};
    char chrarry_NameOfProcess[1024*8]={'\0'};
    char *chrptr_StringToCompare = NULL;
    // static pid_t pid_ProcessIdentifier[16]={(pid_t)-1};
    struct dirent *de_DirEntity = NULL;
    DIR *dir_proc = NULL;

    long (*CompareFunction)(const char*, const char *, int);

    if (intExactMatch)
        CompareFunction = &strcmp_Wrapper;
    else
        CompareFunction = &strstr_Wrapper;

    dir_proc = opendir(PROC_DIRECTORY);
    if (dir_proc == NULL)
    {
        perror("Couldn't open the " PROC_DIRECTORY "directory");
        // return pid ProcessIdentifier;
    }
    //Loop while not NULL
    int i=0;
    while ((de_DirEntity = readdir(dir_proc)))
    {
        if ((de_DirEntity->d_type == DT_DIR))
        {
            if (IsNumeric(de_DirEntity->d_name))
            {
                strcpy(chrarry_CommandLinePath, PROC_DIRECTORY);
                strcat(chrarry_CommandLinePath, de_DirEntity->d_name);
                strcat(chrarry_CommandLinePath, "/cmdline");
                FILE *fd_CmdLineFile = fopen(chrarry_CommandLinePath,"rt"); //open the file for reading text 
                if (fd_CmdLineFile)
                {
                    fscanf(fd_CmdLineFile, "%s", chrarry_NameOfProcess); //read from /proc/<NR>/cmdline 
                    fclose(fd_CmdLineFile);                             //close the file prior to exitingthe routine
                    if (strrchr(chrarry_NameOfProcess, '/'))
                        chrptr_StringToCompare = strrchr(chrarry_NameOfProcess, '/') + 1;
                    else
                        chrptr_StringToCompare = chrarry_NameOfProcess;
                    //printf("Process name: s\n", chrarry_Name0fProcess);
                    //这个是全路径·比如/bin/ls
                    //printf("Pure Process name: $s\n", chrptr_StringToCompare);
                    //这个是纯进程名,比如Ls
                    //这里可以比较全路径名，设置为chrarry_Name0fProcess即可
                    if(CompareFunction(chrptr_StringToCompare, cchrptr_ProcessName, intCaseSensitiveness))
                    {
                        pid_ProcessIdentifier[i]=(pid_t)atoi(de_DirEntity->d_name);
                        // std::coutc<"test aaa: compared pid_name << de_DirEntity->d_name cc std:;endl;
                        i++;
                        if (i > 15)
                        {
                            closedir(dir_proc);
                            break;
                            // return pid_ProcessIdentifier;
                        }
                    }
                }
                memset(chrarry_CommandLinePath, 0, sizeof(chrarry_CommandLinePath));
                memset(chrarry_NameOfProcess, 0, sizeof(chrarry_NameOfProcess));
            }
        }
    }
    closedir(dir_proc);
    // return pid_ProcessIdentifier;
}

// #ifdef __cplusplus
void GetPIDbyName_v2(pid_t *pid_ProcessIdentifier, const char *cchrptr_ProcessName)
{
    return GetPIDbyName_v2(pid_ProcessIdentifier, cchrptr_ProcessName, CASE_INSENSITIVE, INEXACT_MATCH);

}
// #else
// C cannot avarlasd
