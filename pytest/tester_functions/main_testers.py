from tester_functions.bg_listener_testers import helper_test_bg_listener_on
from tester_functions.overlay_view_testers import helper_test_overlay_init, helper_test_overlay_key, helper_test_exit_key, helper_test_wrong_key
from tester_functions.cp_view_testers import helper_test_control_panel_key, helper_test_close_control_panel
from tester_functions.latex_window_testers import helper_test_latex_output_enter
from tester_functions.navbar_component_testers import helper_test_navbar
from tester_functions.unicode_window_testers import helper_test_unicode_search_menu, helper_test_unicode_search_function,helper_test_unicode_copy_paste, helper_test_unicode_copy_via_overlay

def bg_listener_tester(test_env, subtests):
    helper_test_bg_listener_on

# def overlay_tester(test_env, subtests):

#     helper_test_overlay_init(test_env, subtests)

#     helper_test_overlay_key(test_env, subtests)

#     # This will be run right after test_overlay_key()
#     # Thus, Ctrl + D has already been pressed and overlay is on
#     helper_test_exit_key(test_env, subtests)

#     helper_test_wrong_key(test_env, subtests)
    
#     helper_test_control_panel_key(test_env, subtests)

#     helper_test_close_control_panel(test_env)

#     # Redo all of the overlay tests
#     helper_test_overlay_init(test_env, subtests)

#     helper_test_overlay_key(test_env, subtests)

#     # This will be run right after test_overlay_key()
#     # Thus, Ctrl + D has already been pressed and overlay is on
#     helper_test_exit_key(test_env, subtests)

#     helper_test_wrong_key(test_env, subtests)

# def latex_tester(test_env, subtests):
    
#     helper_test_overlay_init(test_env, subtests)

#     helper_test_control_panel_key(test_env, subtests)

#     helper_test_latex_output_enter(test_env, subtests)

# def navbar_tester(test_env, subtests):
    
#     helper_test_overlay_init(test_env, subtests)

#     helper_test_control_panel_key(test_env, subtests)

#     helper_test_navbar(test_env, subtests)

# def unicode_tester(test_env, subtests):

#     helper_test_unicode_search_menu(test_env, subtests)

#     helper_test_unicode_search_function(subtests)

#     helper_test_unicode_copy_paste(subtests)

#     helper_test_unicode_copy_via_overlay(test_env, subtests)