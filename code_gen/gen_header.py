import sys

if __name__ == "__main__":
    with open(sys.argv[1],'w') as f:
        f.write('#pragma once\n\n')
        f.write('#include <Eigen/Dense>\n\n')
        f.write('#include <vector>\n')
        f.write('#include <string>\n\n')
        f.write('/* Type definitions */\n')
        f.write('template <typename T>\n')
        f.write('using vector = std::vector<T>;\n')
        f.write('using string = std::string;\n\n')
        f.write('using VectorXd    = Eigen::VectorXd;\n')
        f.write('using VectorXi    = Eigen::VectorXi;\n')
        f.write('using RowVectorXd = Eigen::RowVectorXd;\n')
        f.write('using RowVectorXi = Eigen::RowVectorXi;\n')
        f.write('using MatrixXd    = Eigen::MatrixXd;\n')
        f.write('using MatrixXi    = Eigen::MatrixXi;\n\n')
        f.write('extern "C" {\n\n')
        # Problem size
        f.write('uint P();\n\n')
        f.write('uint ny(const uint p);\n\n')
        f.write('uint nu(const uint p);\n\n')
        f.write('uint Ns();\n\n')
        f.write('uint Npsi();\n\n')
        # Objective \phi_p
        f.write('double phi(const VectorXd& Y, const VectorXd& U, const VectorXd& S, const uint p);\n\n')
        f.write('bool phi0(const uint p);\n\n');
        f.write('void dphiy(const VectorXd& Y, const VectorXd& U, const VectorXd& S, const uint p, '
                'VectorXd& dphiy);\n\n')
        f.write('void dphiy0(const uint p, VectorXi& dphiy0);\n\n')
        f.write('void dphiu(const VectorXd& Y, const VectorXd& U, const VectorXd& S, const uint p, '
                'VectorXd& dphiu);\n\n')
        f.write('void dphiu0(const uint p, VectorXi& dphiu0);\n\n')
        f.write('void dphis(const VectorXd& Y, const VectorXd& U, const VectorXd& S, const uint p, '
                'VectorXd& dphis);\n\n')
        f.write('void dphis0(const uint p, VectorXi& dphis0);\n\n')
        # Objective \eta_p
        f.write('double eta(const VectorXd& Y0, const VectorXd& Yf, const double t0, const double tf, '
                'const VectorXd& S,\n           const uint p);\n\n')
        f.write('bool eta0(const uint p);\n\n');
        f.write('void detay0(const VectorXd& Y0, const VectorXd& Yf, const double t0, const double tf, '
                'const VectorXd& S,\n            const uint p, VectorXd& detay0);\n\n')
        f.write('void detay00(const uint p, VectorXi& detay00);\n\n')
        f.write('void detayf(const VectorXd& Y0, const VectorXd& Yf, const double t0, const double tf, '
                'const VectorXd& S,\n            const uint p, VectorXd& detayf);\n\n')
        f.write('void detayf0(const uint p, VectorXi& detayf0);\n\n')
        f.write('double detat0(const VectorXd& Y0, const VectorXd& Yf, const double t0, const double tf, '
                'const VectorXd& S,\n              const uint p);\n\n')
        f.write('bool detat00(const uint p);\n\n')
        f.write('double detatf(const VectorXd& Y0, const VectorXd& Yf, const double t0, const double tf, '
                'const VectorXd& S,\n              const uint p);\n\n')
        f.write('bool detatf0(const uint p);\n\n')
        f.write('void detas(const VectorXd& Y0, const VectorXd& Yf, const double t0, const double tf, '
                'const VectorXd& S,\n           const uint p, VectorXd& detas);\n\n')
        f.write('void detas0(const uint p, VectorXi& detas0);\n\n')
        # Dynamics
        f.write('void a(const VectorXd& Y, const VectorXd& U, const VectorXd& S, const uint p, '
                'RowVectorXd& a);\n\n')
        f.write('void a0(const uint p, RowVectorXi& a0);\n\n')
        # Dynamics constraints
        f.write('void Jya(const VectorXd& Y, const VectorXd& U, const VectorXd& S, const uint p, '
                'MatrixXd& Jya);\n\n')
        f.write('void Jya0(const uint p, MatrixXi& Jya0);\n\n')
        f.write('void Jua(const VectorXd& Y, const VectorXd& U, const VectorXd& S, const uint p, '
                'MatrixXd& Jua);\n\n')
        f.write('void Jua0(const uint p, MatrixXi& Jua0);\n\n')
        f.write('void Jsa(const VectorXd& Y, const VectorXd& U, const VectorXd& S, const uint p, '
                'MatrixXd& Jsa);\n\n')
        f.write('void Jsa0(const uint p, MatrixXi& Jsa0);\n\n')
        # Phase interconnection constraints
        f.write('void psi(const vector<VectorXd>& Y0, const vector<VectorXd>& Yf, const VectorXd& t0,\n'
                '         const VectorXd& tf, const VectorXd& S, VectorXd& psi);\n\n')
        f.write('void Jpsiy0(const vector<VectorXd>& Y0, const vector<VectorXd>& Yf, const VectorXd& t0,\n'
                '            const VectorXd& tf, const VectorXd& S, const uint p, MatrixXd& Jpsiy0);\n\n')
        f.write('void Jpsiy00(const uint p, MatrixXi& Jpsiy00);\n\n')
        f.write('void Jpsiyf(const vector<VectorXd>& Y0, const vector<VectorXd>& Yf, const VectorXd& t0,\n'
                '            const VectorXd& tf, const VectorXd& S, const uint p, MatrixXd& Jpsiyf);\n\n')
        f.write('void Jpsiyf0(const uint p, MatrixXi& Jpsiyf0);\n\n')
        f.write('void Jpsit0(const vector<VectorXd>& Y0, const vector<VectorXd>& Yf, const VectorXd& t0,\n'
                '            const VectorXd& tf, const VectorXd& S, const uint p, VectorXd& Jpsit0);\n\n')
        f.write('void Jpsit00(const uint p, VectorXi& Jpsit00);\n\n')
        f.write('void Jpsitf(const vector<VectorXd>& Y0, const vector<VectorXd>& Yf, const VectorXd& t0,\n'
                '            const VectorXd& tf, const VectorXd& S, const uint p, VectorXd& Jpsitf);\n\n')
        f.write('void Jpsitf0(const uint p, VectorXi& Jpsitf0);\n\n')
        f.write('void Jpsis(const vector<VectorXd>& Y0, const vector<VectorXd>& Yf, const VectorXd& t0,\n'
                '           const VectorXd& tf, const VectorXd& S, MatrixXd& Jpsis);\n\n')
        f.write('void Jpsis0(MatrixXi& Jpsis0);\n\n')
        # Signal names
        f.write('vector<string> get_state_names(const uint p);\n\n')
        f.write('vector<string> get_input_names(const uint p);\n\n')
        f.write('}\n')
