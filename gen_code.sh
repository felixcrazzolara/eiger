#!/usr/bin/env bash

# Author: Felix Crazzolara

app_name=$1
code_folder=genCpp

# A function to remove temporary files created by the Maxima script
remove_temp_Maxima_files () {
temp_files=(P Ns ny nu Npsi Y U phi phi0 eta eta0 psi \
            detat0 detat00 detatf detatf0 Jpsis Jpsis0)
temp_files_with_suffix=(a a0 Jya Jya0 Jua Jua0 Jsa Jsa0 \
                        dphiy dphiy0 dphiu dphiu0 dphis dphis0 \
                        dphis dphis0 detay0 detay00 detayf detayf0 \
                        detayf detayf0 detas detas0 \
                        Jpsiy0 Jpsiy00 Jpsiyf Jpsiyf0 \
                        Jpsit0 Jpsit00 Jpsitf Jpsitf0)

for file in ${temp_files[@]}; do
    rm Maxima/${file} 2>/dev/null
done

for file in ${temp_files_with_suffix[@]}; do
    rm Maxima/${file}_* 2>/dev/null
done

}

# Make sure that there are no old files created by Maxima as Maxima appends to files
# created by gentran instead of overwriting them
remove_temp_Maxima_files

# Compute symbolic expressions from Maxima code and generate C++ code from it
cd Maxima
maxima -b ${app_name}.mac >/dev/null
#maxima -b ${app_name}.mac
maxima_exit_code=$(cat /tmp/MAXIMA_EXIT_CODE | sed 's/ //')
if [ ${maxima_exit_code} -eq -1 ]; then
    exit -1
fi
cd ..

# Generate a code segment for variable definitions
mkdir -p ${code_folder}
python code_gen/gen_var_definitions.py `pwd`/${code_folder}/var_defs `pwd`/Maxima/Y `pwd`/Maxima/U

## Turn the generated C++ code into C++ files
# Define the file names
file_name=${code_folder}/${app_name}

# Generate the source file
python code_gen/gen_source.py ${file_name}.cpp `pwd`/Maxima/ `pwd`/${code_folder}/var_defs ${app_name}

# Generate the header file
python code_gen/gen_header.py ${file_name}.hpp

# Remove temporary files
remove_temp_Maxima_files
rm ${code_folder}/var_defs ${code_folder}/var_defs_0f ${code_folder}/var_defs_0f_all
