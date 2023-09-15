
#!/usr/bin/env python3

# 作者: 李霏

# 假设 prospino 程序配置完毕
# 假设 ProspinoIn_{}.txt 已制备好({}是一个表示索引的整型),位于目录 /home/zhd/cs_smodels_test/InputsForProspino/A/ 下, 其中 A 是项目相关的目录名称
import os
import re
import shutil
import pandas as pd

def cross_section(_1st, _2nd, _3rd, _4th, _5th, _6th, _7th, _8th):
    # 选择输出文件 cs13.csv 的部分列索引, 此四列表内容与排序与以前写法一致
    if _1st != _2nd:
        EWkino = ['c1barc2_pb', 'c1barn2_pb', 'c1barn3_pb', 'c1barn4_pb', 'c1barn5_pb', 
                                            'c1c1bar_pb', 'c1c2bar_pb', 'c1n2_pb', 'c1n3_pb', 'c1n4_pb', 'c1n5_pb', 
                                            'c2barn2_pb', 'c2barn3_pb', 'c2barn4_pb', 'c2barn5_pb', 'c2c2bar_pb', 
                                            'c2n2_pb', 'c2n3_pb', 'c2n4_pb', 'c2n5_pb', 
                                            'n2n2_pb', 'n2n3_pb', 'n2n4_pb', 'n2n5_pb', 
                                            'n3n3_pb', 'n3n4_pb', 'n3n5_pb', 'n4n4_pb', 'n4n5_pb', 'n5n5_pb']
    else:    
        EWkino = []    
    if _3rd != _4th:
        Smu = ['smulsmul_pb', 'smursmur_pb', 'snmulsnmul_pb', 'smulPsnmul_pb', 'smulNsnmul_pb']
    else:
        Smu = []    
    if _5th != _6th:
        Se = ['selsel_pb', 'serser_pb', 'snelsnel_pb', 'selPsnel_pb', 'selNsnel_pb']
    else:
        Se = []
    if _7th != _8th:
        Stau = ['sta1sta1_pb', 'sta2sta2_pb', 'sta1psta2m_pb', 'sntalsntal_pb', 
                                            'sta1Psntal_pb', 'sta1Nsntal_pb', 'sta2Psntal_pb', 'sta2Nsntal_pb']
    else:
        Stau = []

    Process_list = list(range(_1st, _2nd))+list(range(_3rd, _4th))+list(range(_5th, _6th))+list(range(_7th, _8th)) 

    for filename in os.listdir(slha_in):   # 获取文件名
        if re.match("ProspinoIn_\d+.txt", filename):     # 提取索引
            Index = int(re.compile(r'\d+').findall(filename)[0])

        for process in Process_list:
            run_dir = root_dir + "/cs_smodels_test/cross_section/prospino" + "/Prospino2_{}".format(str(process))        
            shutil.copy(filename, run_dir + '/prospino.in.les_houches')
            command = " ".join([run_dir + "/prospino_2.run", "> a.txt"])      # prospino 运行命令, Key is here!
            
            # 读写结果
            with open(run_dir + '/prospino.dat', 'r') as f: 
                lines = f.redlines()  
                data = [line.split() for line in lines]           # 将每行内容分割成列表     
                if os.access("{}/prospino_out.csv".format(run_dir), os.F_OK):     
                    data[0].insert(0, '{}'.format(Index))   
                    data=[data[0]]
                    df = pd.DataFrame(data)    # 保存为 .csv          
                    df.to_csv("{}/prospino_out.csv".format(run_dir), mode='a',index=False, header=False)
                else:
                    data = [x for x in data if x !=[]]                
                    data[0], data[1] = data[1], data[0]   # 两行互换, 并附加信息                           
                    data[0].insert(0, 'Index')                
                    data[0].insert(1, 'FSI') 
                    data[1].insert(0, '{}'.format(Index))
                    df = pd.DataFrame(data)     # 保存为.csv              
                    df.to_csv("{}/prospino_out.csv".format(run_dir), mode='w',index=False, header=False)        
        
        NLO_list = [] 
        XS = 0.
        for process in Process_list:       # 根据index索引提取截面并将其添加到列表 NLO_list    
            run_dir = root_dir + "/cs_smodels_test/cross_section/prospino" + "/Prospino2_{}".format(str(process))
            df = pd.read_csv("{}/prospino_out.csv".format(run_dir))
            df.set_index('Index',inplace=True)    
            NLO = df.loc[Index].iloc[-1]
            NLO_list.append(NLO)
        for xs in NLO_list:    # 计算总截面
            XS += xs
        NLO_list.append(XS)
        
        # 生成最终的 cs13.csv 表格
        data = [[str(Index)] + NLO_list]
        columns=['Index'] + EWkino + Smu + Se + Stau +['XS_pb']
        df = pd.DataFrame(data,columns=columns)
        if os.access("{}/cs13.csv".format(program_dir), os.F_OK):
            df.to_csv("{}/cs13.csv".format(program_dir), sep=',', mode='a', header=False, index=False)
        else:
            df.to_csv("{}/cs13.csv".format(program_dir), sep=',', mode='w', header=True, index=False)     


# 计算一个点的所有程截面,然后求总截面
if __name__ == '__main__':
    root_dir = "/home/zhd"
    program_dir = root_dir + '/cs_smodels_test'
    slha_dir = root_dir + '/cs_smodels_test/InputsForProspino/A' 
    cross_section(1, 31, 31, 36, 36, 41, 41, 49)  