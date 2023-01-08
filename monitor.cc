
#include <iostream>
#include <stdio.h>
#include <unistd.h>
#include <string.h>
#include <stdlib.h>
#include <iomanip>
#include <bitset>
#include <vector>
#include <string>
#include <time.h>
#define VMRSS_LINE 22
#define VMSIZE_LINE 18
#define PROCESS_ITEM 14

void GetPIDbyName_v2(pid_t *pid_ProcessIdentifier, const char *cchrptr_ProcessName, int intCaseSensitiveness, int intExactMatch);

typedef struct {
    uint64_t user;
    uint64_t nice;
    uint64_t sys;
    uint64_t idle;
    uint64_t iowait;
    uint64_t irq;
    uint64_t softirq;
}Sys_Cpu_stat_t;

typedef struct{
    int pid;
    uint64_t user;
    uint64_t sys;
    uint64_t cutime;
    uint64_t cstime;
}Proc_Cpu_stat_t;
//获取第N项开始的指针
const char* get_items(const char*buffer ,unsigned int item){
    const char *p =buffer;
    int len = strlen(buffer);
    unsigned int count = 0;
    for(int i=0; i<len; i++){
        if(' ' == *p){
            count ++;
            if(count == (item -1)){
                p++;
                break;
            }
        }
        p++;
    }
    return p;
}
float get_num_cpu(){
    float num_cpu = 0.0;
    char line_buff[512]={0};
    FILE *fd;
    fd =fopen("/proc/stat","r");
    if(nullptr == fd){
        fclose(fd);
        return 0;
    }
    char name[64];
    uint64_t value;
    while (true){
        fgets(line_buff,sizeof(line_buff),fd);
        sscanf(line_buff,"%s %lu", name, &value);
        if (name[0]=='c' and name[1]=='p'){
            num_cpu += 1.0;
        }
        else{
            break;
        }
    }
    return(num_cpu-1.0);
}
uint64_t get_sys_cpu_sum(){
    FILE *fd = fopen("/proc/stat", "r");
    char buff[70];
    if (fd != NULL)
    {
        fgets(buff, sizeof(buff),fd);
        fclose(fd);
        Sys_Cpu_stat_t cpu_t;
        sscanf(buff,"cpu  %lu %lu %lu %lu %lu %lu %lu", &cpu_t.user, &cpu_t.nice, &cpu_t.sys, &cpu_t.idle, &cpu_t.iowait, &cpu_t.irq, &cpu_t.softirq);
        double sum=cpu_t.user+cpu_t.nice+cpu_t.sys+cpu_t.idle+cpu_t.iowait+cpu_t.irq+cpu_t.softirq;
        return sum;
    }
    return -1;
}
uint64_t get_sys_cpu_idle(){
    FILE *fd = fopen("/proc/stat", "r");
    char buff[70];
    if (fd != NULL)
    {
        fgets(buff, sizeof(buff), fd);
        fclose(fd);
        Sys_Cpu_stat_t cpu_t;
        sscanf(buff,"cpu %lu %lu %lu %lu %lu %lu %lu", &cpu_t.user, &cpu_t.nice, &cpu_t.sys, &cpu_t.idle, &cpu_t.iowait, &cpu_t.irq, &cpu_t.softirq);
        return cpu_t.idle;
    }
    return -1;
}
uint64_t get_pid_cpu(int pid){
    char pid_s[64] = {0};
    if (pid == 0){
        sprintf(pid_s, "self");
    }
    else if (pid == -1){
        return 0;
    }
    else{
        sprintf(pid_s, "%i", pid);
    }
    char filename[128]= {0};
    sprintf(filename,"/proc/%s/stat",pid_s);
    Proc_Cpu_stat_t cpu_t;
    FILE *fd = fopen(filename, "r");
    char buff[1024];
    if (fd != NULL)
    {
        fgets(buff, sizeof(buff), fd);
        fclose(fd);
        sscanf(buff, "%i", &cpu_t.pid);
        const char *pid_cpu = get_items(buff, PROCESS_ITEM);
        sscanf(pid_cpu,"%lu %lu", &cpu_t.user, &cpu_t.sys);
        // std::cout << cpu t.user <<""<< cpu t.sys<< "" << cpu_t.cutime<</1""<< cpu_t.cstime << std::endl;
        return (cpu_t.user+cpu_t.sys);
    }
    return 0;
}
// 总内存大小
uint64_t get_mem_total(){
    uint64_t mem_total;
    char line_buff[512]={0};
    FILE *fd;
    fd = fopen("/proc/meminfo", "r");
    if(nullptr == fd){
        fclose(fd);
        return 0;
    }
    fgets(line_buff, sizeof(line_buff), fd);
    sscanf(line_buff,"MemTotal: %lu", &mem_total);
    fclose(fd);
    return mem_total;
}
// 系统内存占用
float get_sys_pmem(){
    float pmem;
    char line_buff[512]={0};
    FILE *fd;
    fd =fopen("/proc/meminfo","r");
    if(nullptr == fd){
        fclose(fd);
        return 0;
    }
    char name[64];
    uint64_t value;
    uint64_t mem_total;
    uint64_t mem_avail = 0;
    for (int i=0;i<6;i++){
        fgets(line_buff,sizeof(line_buff),fd);
        sscanf(line_buff,"%s %lu",name,&value);
        if (i == 0){
            mem_total = value;
        }
        if (i ==1 or i ==3 or i== 4){
            mem_avail += value;
        }
    }
    pmem = 100.0-(mem_avail*100.0/mem_total);
    fclose(fd);
    return pmem;
}
//获取进程占用内存
float get_proc_mem(pid_t pid){
    char file_name[64]={0};
    FILE *fd;
    char line_buff[512]={0};
    sprintf(file_name,"/proc/%d/status",pid);
    fd =fopen(file_name,"r");
    if(nullptr ==fd){
        // fclose(fd);
        return 0;
    }
    char name[64];
    uint64_t vmrss;
    for (int i=0; i<VMRSS_LINE-1; i++){
        fgets(line_buff,sizeof(line_buff),fd);
    }
    fgets(line_buff,sizeof(line_buff),fd);
    sscanf(line_buff,"%s %lu",name,&vmrss);
    fclose(fd);
    uint64_t mem_total = get_mem_total();
    if (vmrss >mem_total){
        return 0.0;
    }
    float pmem = vmrss*100.0/mem_total;
    return pmem;
}
// 获取进程占用虚拟内存
unsigned int get_proc_virtualmem(unsigned int pid){
    char file_name[64]={0};
    FILE *fd;
    char line_buff[512]={0};
    sprintf(file_name,"/proc/%d/status",pid);
    fd =fopen(file_name,"r");
    if(nullptr == fd){
        fclose(fd);
        return 0;
    }
    char name[64];
    int vmsize;
    for (int i=0;i<VMSIZE_LINE-1;i++){
        fgets(line_buff,sizeof(line_buff),fd);
    }
    fgets(line_buff,sizeof(line_buff),fd);
    sscanf(line_buff,"%s %d",name,&vmsize);
    fclose(fd);
    return vmsize;
}
int main()
{
    std::vector<std::string> app_list={"example_app","test_"};
    float num_cpu = get_num_cpu();
    char a_c[256];
    pid_t pid_tmp[64];
    std::string name_pid[64]={};
    uint64_t aa[64]={};
    uint64_t aaa[64]={};
    float pcpu = 0.0;
    float pcpu_pid = 0.0;
    float pmem_pid = 0.0;
    float pmem = 0.0;
    time_t ts = 1;
    time_t ts_last = 0;
    FILE * log;
    log = fopen("./monitor.log","w");
    char line2log[1024];
    if (NULL == log)
    {
        std::cout <<"can not write ./monitor.log !"<< std::endl;
        fclose (log);
    }
    fclose(log);
    std::cout <<"[monitor]Start to monitor!"<< std::endl;
    while (true)
    {
        ts=time(NULL);
        if (ts != ts_last){
            log = fopen("./monitor.log","a");
            // 每次重新查找pid
            int k = 0;
            for (std::string a : app_list){
                strcpy(a_c,a.c_str());
                pid_t pid_list[16]= {0};
                pid_t* p = pid_list;
                GetPIDbyName_v2(p,a_c,1,0);
                for (int i = 0; i < 16; i++)
                {
                    // test output
                    // std::cout << "test:pid list "<< k <<" th pid:"<< pli] << std::endl;
                    if (pid_list[i] != 0)
                    {
                        pid_tmp[k]=pid_list[i];
                        name_pid[k]= a + '_' + std::to_string(pid_list[i]);
                        k++;
                    }
                    else{
                        break;
                    }
                }
            }
            // pid = GetPIDbyName(a, 1,1);
            // 获取cpu负载
            uint64_t sys_cpu_total1=get_sys_cpu_sum();
            uint64_t sys_cpu_idle1=get_sys_cpu_idle();
            // uint64 t pid cpu1=get_pid_cpu(pid);
            for (int j =0; j<64; j++){
                if (pid_tmp[j] == 0){
                    break;
                }
                aa[j]=get_pid_cpu(pid_tmp[j]);
            }
            usleep(500000);
            uint64_t sys_cpu_total2=get_sys_cpu_sum();
            uint64_t sys_cpu_idle2=get_sys_cpu_idle();
            // uint64_t pid_cpu2=get_pid_cpu(pid);
            for (int j=0;j<64;j++){
                if (pid_tmp[j] == 0){
                    break;
                }
                aaa[j]=get_pid_cpu(pid_tmp[j]);
            }
            if(0 != sys_cpu_total2-sys_cpu_total1){
                pcpu=100.0*(1.0-(sys_cpu_idle2-sys_cpu_idle1+0.0)/(sys_cpu_total2-sys_cpu_total1));
                pmem=get_sys_pmem();
                // std::cout << std::fixed << std::setprecision(3) <ts<":Sys cpus:"<< std::setw(8)<< pcDu << "Sys mems:"c< std::setw(8)<< pmem;
                sprintf(line2log, "%li : Sys cpu%%: %8.3f mem%%: %8.3f",ts,pcpu,pmem);
                fputs(line2log,log);
                k=0;
                for (std::string a : name_pid){
                    if (a == "")
                    {
                        break;
                    }
                    strcpy(a_c, a.c_str());
                    uint64_t diff_cpu_pid;
                    if (aaa[k] != 0){
                        diff_cpu_pid = aaa[k] -aa[k];
                    }
                    else{
                        diff_cpu_pid = 0;
                    }
                    pcpu_pid=num_cpu * 100.0 *(diff_cpu_pid+0.0)/(sys_cpu_total2-sys_cpu_total1);
                    pmem_pid=get_proc_mem(pid_tmp[k]);
                    sprintf(line2log, " >>> %s <<< process cpu%%: %8.3f mem%%: %8.3f", a_c, pcpu_pid, pmem_pid);
                    fputs (line2log, log);
                    k++;
                }
                // std::cout << std::endl;
            }
            fputs ("\n", log);
            fclose(log);
            ts_last=ts;
        }
        // 1++;
        usleep(1000);
    }
    return 0;
}

