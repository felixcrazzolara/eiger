import sys
import re

def write_fun_content(f,fun_name,from_single_file=False,mat_expr=True,stacked_mat=False,def_YUS=False,
                      def_Y0Yft0tfS=False,def_Y0Yft0tfS_all=False):
    if def_YUS:
        f.write(YUS_def_str)
    if def_Y0Yft0tfS:
        f.write(Y0f_def_str)
        f.write('    //--- Definition of initial and final times ---//\n')
        for p in range(P):
            f.write(f'    // Phase {p+1}\n')
            f.write(f'    double t0{p+1};\n')
            f.write(f'    double tf{p+1};\n\n')
        for p in range(P):
            f.write(f'    // Phase {p+1}\n')
            if p == 0:
                f.write('    if (p == 0) {\n')
                f.write(f'        t0{p+1} = t0;\n')
                f.write(f'        tf{p+1} = tf;\n')
                if p == P-1:
                    f.write('    }\n')
            else:
                f.write('    }'+f' else if (p == {p}) '+'{\n')
                f.write(f'        t0{p+1} = t0;\n')
                f.write(f'        tf{p+1} = tf;\n')
                f.write('    }\n')
            f.write('\n')
    if def_Y0Yft0tfS_all:
        f.write(Y0f_all_def_str)
        f.write('    //--- Definition of initial and final times ---//\n')
        for p in range(P):
            f.write(f'    // Phase {p+1}\n')
            f.write(f'    const double& t0{p+1} = t0({p});\n')
            f.write(f'    const double& tf{p+1} = tf({p});\n\n')

    f.write(f'    //--- Computation of {fun_name} ---//\n')
    if from_single_file:
        with open(sys.argv[2]+fun_name) as ff:
            lines = ff.readlines()
            if mat_expr:
                for line in lines:
                    line    = line.strip()
                    lhs,rhs = line.split('=')
                    assert(lhs[:5]=='expr(')
                    assert(lhs[-1]==')')
                    idx0,idx1 = [int(c)-1 for c in lhs[5:-1].split(',')]
                    line      = f'{fun_name}(' + str(idx0) + ',' + str(idx1) + ') = ' + rhs + '\n'
                    f.write('    '+line)
                f.write('}\n\n')
            else:
                for p in range(P):
                    if p == 0:
                        f.write('    if (p == 0) {\n')
                    else:
                        f.write('    }'+f' else if (p == {p}) '+'{\n')
                    line = lines[p].strip()
                    line = re.sub('unknown','false',line)
                    f.write('        return '+line+';\n');
                f.write('    }\n}\n\n')
    else:
        if stacked_mat:
            col_offset = 0
            for p in range(P):
                with open(sys.argv[2]+f'{fun_name}_{p+1}') as ff:
                    max_col_idx = -1
                    for line in ff.readlines():
                        line    = line.strip()
                        lhs,rhs = line.split('=')
                        assert(lhs[:5]=='expr(')
                        assert(lhs[-1]==')')
                        idx0,idx1 = [int(c)-1 for c in lhs[5:-1].split(',')]
                        if idx1 > max_col_idx:
                            max_col_idx = idx1
                        rhs       = re.sub('unknown','0',rhs)
                        line      = f'{fun_name}('+str(idx0)+','+str(idx1+col_offset)+') = '+rhs+'\n'
                        f.write('    '+line)
                    col_offset += max_col_idx+1
            f.write('}\n\n')
        else:
            for p in range(P):
                if p == 0:
                    f.write('    if (p == 0) {\n')
                else:
                    f.write('    }'+f' else if (p == {p}) '+'{\n')
                with open(sys.argv[2]+f'{fun_name}_{p+1}') as ff:
                    for line in ff.readlines():
                        line    = line.strip()
                        lhs,rhs = line.split('=')
                        assert(lhs[:5]=='expr(')
                        assert(lhs[-1]==')')
                        idx0,idx1 = [int(c)-1 for c in lhs[5:-1].split(',')]
                        rhs       = re.sub('unknown','0',rhs)
                        line      = f'{fun_name}(' + str(idx0) + ',' + str(idx1) + ') = ' + rhs + '\n'
                        f.write('        '+line)
            f.write('    }\n}\n\n')

def write_sig_name_fun_content(f,n):
    with open(sys.argv[2]+n,'r') as ff:
        ll_str  = ff.readlines()[0].strip()
        lt_str  = ll_str[1:-1]
        l_str_l = ['['+l_str.strip(' ,') for l_str in lt_str.split('[')[1:]]
        sig_names = []
        for l_str in l_str_l:
            sig_name_str_l = [_.strip() for _ in l_str[1:-1].split(',')]
            sig_names     += [sig_name_str_l]
        for p in range(P):
            if p == 0:
                f.write('    if (p == 0) {\n')
            else:
                f.write('    }'+f' else if (p == {p}) '+'{\n')
            f.write('        return {')
            for i,sig_name in enumerate(sig_names[p]):
                f.write('"'+sig_name+'"')
                if i != len(sig_names[p])-1:
                    f.write(',')
            f.write('};\n')
        f.write('    }\n}\n\n')

if __name__ == "__main__":
    # Get the variables definitions
    with open(sys.argv[3],'r') as f:
        lines = f.readlines()
        YUS_def_str = ""
        for line in lines:
            YUS_def_str += '    '+line
    with open(sys.argv[3]+'_0f','r') as f:
        lines = f.readlines()
        Y0f_def_str = ""
        for line in lines:
            Y0f_def_str += '    '+line
    with open(sys.argv[3]+'_0f_all','r') as f:
        lines = f.readlines()
        Y0f_all_def_str = ""
        for line in lines:
            Y0f_all_def_str += '    '+line

    with open(sys.argv[1],'w') as f:
        f.write('#include <cmath>\n\n')
        f.write('#include \"'+sys.argv[4]+'.hpp\"\n\n')
        f.write('extern "C" {\n\n')
        # Problem size
        with open(sys.argv[2]+'P','r') as ff:
            P = int(ff.readlines()[0].strip())
            f.write('uint P() {\n')
            f.write(f'    return {P};\n')
            f.write('}\n\n')
        with open(sys.argv[2]+'Ns','r') as ff:
            Ns = int(ff.readlines()[0].strip())
            f.write('uint Ns() {\n')
            f.write(f'    return {Ns};\n')
            f.write('}\n\n')
        with open(sys.argv[2]+'Npsi','r') as ff:
            Npsi = int(ff.readlines()[0].strip())
            f.write('uint Npsi() {\n')
            f.write(f'    return {Npsi};\n')
            f.write('}\n\n')
        f.write('uint ny(const uint p) {\n')
        write_fun_content(f,'ny',from_single_file=True,mat_expr=False)
        f.write('uint nu(const uint p) {\n')
        write_fun_content(f,'nu',from_single_file=True,mat_expr=False)
        # Objective \phi_p
        f.write('double phi(const VectorXd& Y, const VectorXd& U, const VectorXd& S, const uint p) {\n')
        write_fun_content(f,"phi",from_single_file=True,mat_expr=False,def_YUS=True)
        f.write('bool phi0(const uint p) {\n')
        write_fun_content(f,"phi0",from_single_file=True,mat_expr=False);
        f.write('void dphiy(const VectorXd& Y, const VectorXd& U, const VectorXd& S, const uint p, '
                'VectorXd& dphiy) {\n')
        write_fun_content(f,"dphiy",def_YUS=True)
        f.write('void dphiy0(const uint p, VectorXi& dphiy0) {\n')
        write_fun_content(f,"dphiy0")
        f.write('void dphiu(const VectorXd& Y, const VectorXd& U, const VectorXd& S, const uint p, '
                'VectorXd& dphiu) {\n')
        write_fun_content(f,"dphiu",def_YUS=True)
        f.write('void dphiu0(const uint p, VectorXi& dphiu0) {\n')
        write_fun_content(f,"dphiu0")
        f.write('void dphis(const VectorXd& Y, const VectorXd& U, const VectorXd& S, const uint p, '
                'VectorXd& dphis) {\n')
        write_fun_content(f,"dphis",def_YUS=True)
        f.write('void dphis0(const uint p, VectorXi& dphis0) {\n')
        write_fun_content(f,"dphis0")
        # Objective \eta_p
        f.write('double eta(const VectorXd& Y0, const VectorXd& Yf, const double t0, const double tf, '
                'const VectorXd& S,\n           const uint p) {\n')
        write_fun_content(f,"eta",from_single_file=True,mat_expr=False,def_Y0Yft0tfS=True)
        f.write('bool eta0(const uint p) {\n')
        write_fun_content(f,"eta0",from_single_file=True,mat_expr=False);
        f.write('void detay0(const VectorXd& Y0, const VectorXd& Yf, const double t0, const double tf, '
                'const VectorXd& S,\n            const uint p, VectorXd& detay0) {\n')
        write_fun_content(f,"detay0",def_Y0Yft0tfS=True)
        f.write('void detay00(const uint p, VectorXi& detay00) {\n')
        write_fun_content(f,"detay00")
        f.write('void detayf(const VectorXd& Y0, const VectorXd& Yf, const double t0, const double tf, '
                'const VectorXd& S,\n            const uint p, VectorXd& detayf) {\n')
        write_fun_content(f,"detayf",def_Y0Yft0tfS=True)
        f.write('void detayf0(const uint p, VectorXi& detayf0) {\n')
        write_fun_content(f,"detayf0")
        f.write('double detat0(const VectorXd& Y0, const VectorXd& Yf, const double t0, const double tf, '
                'const VectorXd& S,\n              const uint p) {\n')
        write_fun_content(f,"detat0",from_single_file=True,mat_expr=False,def_Y0Yft0tfS=True)
        f.write('bool detat00(const uint p) {\n')
        write_fun_content(f,"detat00",from_single_file=True,mat_expr=False)
        f.write('double detatf(const VectorXd& Y0, const VectorXd& Yf, const double t0, const double tf, '
                'const VectorXd& S,\n              const uint p) {\n')
        write_fun_content(f,"detatf",from_single_file=True,mat_expr=False,def_Y0Yft0tfS=True)
        f.write('bool detatf0(const uint p) {\n')
        write_fun_content(f,"detatf0",from_single_file=True,mat_expr=False)
        f.write('void detas(const VectorXd& Y0, const VectorXd& Yf, const double t0, const double tf, '
                'const VectorXd& S,\n           const uint p, VectorXd& detas) {\n')
        write_fun_content(f,"detas",def_Y0Yft0tfS=True)
        f.write('void detas0(const uint p, VectorXi& detas0) {\n')
        write_fun_content(f,"detas0")
        # Dynamics
        f.write('void a(const VectorXd& Y, const VectorXd& U, const VectorXd& S, const uint p, '
                'RowVectorXd& a) {\n')
        write_fun_content(f,"a",def_YUS=True)
        f.write('void a0(const uint p, RowVectorXi& a0) {\n')
        write_fun_content(f,"a0")
        # Dynamics constraints
        f.write('void Jya(const VectorXd& Y, const VectorXd& U, const VectorXd& S, const uint p, '
                'MatrixXd& Jya) {\n')
        write_fun_content(f,"Jya",def_YUS=True)
        f.write('void Jya0(const uint p, MatrixXi& Jya0) {\n')
        write_fun_content(f,"Jya0")
        f.write('void Jua(const VectorXd& Y, const VectorXd& U, const VectorXd& S, const uint p, '
                'MatrixXd& Jua) {\n')
        write_fun_content(f,"Jua",def_YUS=True)
        f.write('void Jua0(const uint p, MatrixXi& Jua0) {\n')
        write_fun_content(f,"Jua0")
        f.write('void Jsa(const VectorXd& Y, const VectorXd& U, const VectorXd& S, const uint p, '
                'MatrixXd& Jsa) {\n')
        write_fun_content(f,"Jsa",def_YUS=True)
        f.write('void Jsa0(const uint p, MatrixXi& Jsa0) {\n')
        write_fun_content(f,"Jsa0")
        # Phase interconnection constraints
        f.write('void psi(const vector<VectorXd>& Y0, const vector<VectorXd>& Yf, const VectorXd& t0, '
                'const VectorXd& tf, const VectorXd& S, VectorXd& psi) {\n')
        write_fun_content(f,"psi",from_single_file=True,mat_expr=True,def_Y0Yft0tfS_all=True)
        f.write('void Jpsiy0(const vector<VectorXd>& Y0, const vector<VectorXd>& Yf, const VectorXd& t0,\n'
                '            const VectorXd& tf, const VectorXd& S, const uint p, MatrixXd& Jpsiy0) {\n')
        write_fun_content(f,"Jpsiy0",def_Y0Yft0tfS_all=True)
        f.write('void Jpsiy00(const uint p, MatrixXi& Jpsiy00) {\n')
        write_fun_content(f,"Jpsiy00")
        f.write('void Jpsiyf(const vector<VectorXd>& Y0, const vector<VectorXd>& Yf, const VectorXd& t0,\n'
                '            const VectorXd& tf, const VectorXd& S, const uint p, MatrixXd& Jpsiyf) {\n')
        write_fun_content(f,"Jpsiyf",def_Y0Yft0tfS_all=True)
        f.write('void Jpsiyf0(const uint p, MatrixXi& Jpsiyf0) {\n')
        write_fun_content(f,"Jpsiyf0")
        f.write('void Jpsit0(const vector<VectorXd>& Y0, const vector<VectorXd>& Yf, const VectorXd& t0,\n'
                '            const VectorXd& tf, const VectorXd& S, const uint p, VectorXd& Jpsit0) {\n')
        write_fun_content(f,"Jpsit0",def_Y0Yft0tfS_all=True)
        f.write('void Jpsit00(const uint p, VectorXi& Jpsit00) {\n')
        write_fun_content(f,"Jpsit00")
        f.write('void Jpsitf(const vector<VectorXd>& Y0, const vector<VectorXd>& Yf, const VectorXd& t0,\n'
                '            const VectorXd& tf, const VectorXd& S, const uint p, VectorXd& Jpsitf) {\n')
        write_fun_content(f,"Jpsitf",def_Y0Yft0tfS_all=True)
        f.write('void Jpsitf0(const uint p, VectorXi& Jpsitf0) {\n')
        write_fun_content(f,"Jpsitf0")
        f.write('void Jpsis(const vector<VectorXd>& Y0, const vector<VectorXd>& Yf, const VectorXd& t0,\n'
                '           const VectorXd& tf, const VectorXd& S, MatrixXd& Jpsis) {\n')
        write_fun_content(f,"Jpsis",from_single_file=True,def_Y0Yft0tfS_all=True)
        f.write('void Jpsis0(MatrixXi& Jpsis0) {\n')
        write_fun_content(f,"Jpsis0",from_single_file=True)
        # Signal names
        f.write('vector<string> get_state_names(const uint p) {\n')
        write_sig_name_fun_content(f,'Y')
        f.write('vector<string> get_input_names(const uint p) {\n')
        write_sig_name_fun_content(f,'U')
        f.write('}\n')
