import sys
import json

if __name__ == "__main__":
    # Get the state definition
    Y_vars_l = []
    with open(sys.argv[2],'r') as f:
        Y_str_l  = f.readlines()[0].strip()[1:-1].split('[')[1:]
        Y_str_l  = [Y_str.strip(" ,]") for Y_str in Y_str_l]
        for Y_str in Y_str_l:
            Y_vars_l.append([s.strip() for s in Y_str.split(',')])

    # Get the input definition
    U_vars_l = []
    with open(sys.argv[3],'r') as f:
        U_str_l = f.readlines()[0].strip()[1:-1].split('[')[1:]
        U_str_l = [U_str.strip(" ,]") for U_str in U_str_l]
        for U_str in U_str_l:
            U_vars_l.append([s.strip() for s in U_str.split(',')])

    # Write code to a file for the variable definitions of the states, inputs and static variables
    with open(sys.argv[1],'w') as f:
        f.write('//--- Definition of the states ---//\n')
        y_var_l = []
        for p in range(len(Y_vars_l)):
            f.write(f'// Phase {p+1}\n')
            for i,y in enumerate(Y_vars_l[p]):
                if y in y_var_l:
                    f.write(f'/*double {y};*/\n')
                else:
                    f.write(f'double {y};\n')
                    y_var_l.append(y)
            f.write('\n')
        for p in range(len(Y_vars_l)):
            f.write(f'// Phase {p+1}\n')
            if p == 0:
                f.write('if (p == 0) {\n')
                for i,y in enumerate(Y_vars_l[p]):
                    f.write(f'    {y} = Y({i});\n')
                if p == len(Y_vars_l)-1:
                    f.write('}\n')
            else:
                f.write('}'+f' else if (p == {p}) '+'{\n')
                for i,y in enumerate(Y_vars_l[p]):
                    f.write(f'    {y} = Y({i});\n')
                f.write('}\n')
            f.write('\n')
        f.write('//--- Definition of the inputs ---//\n')
        u_var_l = []
        for p in range(len(U_vars_l)):
            f.write(f'// Phase {p+1}\n')
            for i,u in enumerate(U_vars_l[p]):
                if u in u_var_l:
                    f.write(f'/*double {u};*/\n')
                else:
                    f.write(f'double {u};\n')
                    u_var_l.append(u)
            f.write('\n')
        for p in range(len(U_vars_l)):
            f.write(f'// Phase {p+1}\n')
            if p == 0:
                f.write('if (p == 0) {\n')
                for i,u in enumerate(U_vars_l[p]):
                    f.write(f'    {u} = U({i});\n')
                if p == len(U_vars_l)-1:
                    f.write('}\n')
            else:
                f.write('}'+f' else if (p == {p}) '+'{\n')
                for i,u in enumerate(U_vars_l[p]):
                    f.write(f'    {u} = U({i});\n')
                f.write('}\n')
            f.write('\n')

    # Write code to a file for the variable definitions of the initial and final states
    with open(sys.argv[1]+'_0f','w') as f:
        f.write('//--- Definition of the initial and final states ---//\n')
        for p in range(len(Y_vars_l)):
            f.write(f'// Phase {p+1}\n')
            for i,y in enumerate(Y_vars_l[p]):
                f.write(f'double {y}0{p+1};\n')
                f.write(f'double {y}f{p+1};\n')
            f.write('\n')
        for p in range(len(Y_vars_l)):
            f.write(f'// Phase {p+1}\n')
            if p == 0:
                f.write('if (p == 0) {\n')
                for i,y in enumerate(Y_vars_l[p]):
                    f.write(f'    {y}0{p+1} = Y0({i});\n')
                    f.write(f'    {y}f{p+1} = Yf({i});\n')
                if p == len(Y_vars_l)-1:
                    f.write('}\n')
            else:
                f.write('}'+f' else if (p == {p}) '+'{\n')
                for i,y in enumerate(Y_vars_l[p]):
                    f.write(f'    {y}0{p+1} = Y0({i});\n')
                    f.write(f'    {y}f{p+1} = Yf({i});\n')
                f.write('}\n')
            f.write('\n')

    # Write code to a file for the variable definitions of all initial and final states
    with open(sys.argv[1]+'_0f_all','w') as f:
        f.write('//--- Definition of the initial and final states ---//\n')
        for p in range(len(Y_vars_l)):
            f.write(f'// Phase {p+1}\n')
            for i,y in enumerate(Y_vars_l[p]):
                f.write(f'const double& {y}0{p+1} = Y0[{p}]({i});\n')
                f.write(f'const double& {y}f{p+1} = Yf[{p}]({i});\n')
            f.write('\n')

