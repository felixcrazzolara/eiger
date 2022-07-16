/* 
 * Author: Felix Crazzolara
 */ 
#include "list.hpp"

#include "brachistochrone.hpp"

using namespace cs;

/* Type definitions */
using uint = unsigned int;

/* Parameters */
constexpr uint NUM_MESH_INTERVALS_PER_PHASE             = 8;
constexpr uint NUM_COLLOCATION_POINTS_PER_MESH_INTERVAL = 5;

extern "C" {

List get_num_mesh_intervals() {
    return List(Range(P()),[](auto p){
        return NUM_MESH_INTERVALS_PER_PHASE;
    });
}

List get_num_collocation_points() {
    return List(Range(P()),[](auto p){
        return List(Range(NUM_MESH_INTERVALS_PER_PHASE),[](auto k){
            return NUM_COLLOCATION_POINTS_PER_MESH_INTERVAL;
        });
    });
}

List get_lower_state_bounds() {
    return List(Range(P()),[](auto p){
        return List(0.0,-1.0,0.0);
    });
}

List get_upper_state_bounds() {
    return List(Range(P()),[](auto p){
        return List(1.0,0.45,20.0);
    });
}

List get_lower_initial_state_bounds() {
    return List(Range(P()),[](auto p){
        return List(0.0,0.45,0.0);
    });
}

List get_upper_initial_state_bounds() {
    return List(Range(P()),[](auto p){
        return List(0.0,0.45,0.0);
    });
}

List get_lower_final_state_bounds() {
    return List(Range(P()),[](auto p){
        return List(1.0,0.0,0.0);
    });
}

List get_upper_final_state_bounds() {
    return List(Range(P()),[](auto p){
        return List(1.0,0.0,20.0);
    });
}

List get_lower_input_bounds() {
    return List(Range(P()),[](auto p){
        return List(-M_PI/2.0);
    });
}

List get_upper_input_bounds() {
    return List(Range(P()),[](auto p){
        return List(M_PI/2.0);
    });
}

List get_lower_initial_time_bounds() {
    return List(0.0);
}

List get_upper_initial_time_bounds() {
    return List(0.0);
}

List get_lower_final_time_bounds() {
    return List(0.0);
}

List get_upper_final_time_bounds() {
    return List(100.0);
}

List get_lower_static_variables_bounds() {
    return List();
}

List get_upper_static_variables_bounds() {
    return List();
}

List get_initial_state_guess() {
    return List(Range(P()),[](const auto& p) {
        return List(Range(NUM_MESH_INTERVALS_PER_PHASE),[&p](const auto& k) {
            const uint L = k == NUM_MESH_INTERVALS_PER_PHASE - 1 ? 
                NUM_COLLOCATION_POINTS_PER_MESH_INTERVAL + 1 :
                NUM_COLLOCATION_POINTS_PER_MESH_INTERVAL;
            return List(Range(L),[&p](const auto& l) {
                return List(Range(ny(p)),[](const auto& i) {
                    return 0.0;
                });
            });
        });
    });
}

List get_initial_input_guess() {
    return List(Range(P()),[](const auto& p) {
        return List(Range(NUM_MESH_INTERVALS_PER_PHASE),[&p](const auto& k) {
            return List(Range(NUM_COLLOCATION_POINTS_PER_MESH_INTERVAL),[&p](const auto& l) {
                return List(Range(nu(p)),[](const auto& i) {
                    return 0.0;
                });
            });
        });
    });
}

List initial_initial_time_guess() {
    return List(Range(P()),[](const auto& p) {
        return 0.0;
    });
}

List initial_final_time_guess() {
    return List(Range(P()),[](const auto& p) {
        return 2.0;
    });
}

List initial_static_variables_guess() {
    return List(Range(Ns()),[](const auto& s) {
        return 0.0;
    });
}

}
