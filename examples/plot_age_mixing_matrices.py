"""
Plot the generated age-specific contact matrix.
"""

import synthpops as sp
# import sciris as sc

import matplotlib as mplt
import matplotlib.pyplot as plt
import cmocean
import cmasher as cmr
import seaborn as sns

import os
from collections import Counter
import pytest


if not sp.config.full_data_available:
    pytest.skip("Data not available, tests not possible", allow_module_level=True)

# Pretty fonts

try:
    fontstyle = 'Roboto_Condensed'
    mplt.rcParams['font.family'] = fontstyle.replace('_', ' ')
except:
    mplt.rcParams['font.family'] = 'Roboto'
mplt.rcParams['font.size'] = 16


def test_plot_generated_contact_matrix(setting_code='H', n=5000, aggregate_flag=True, logcolors_flag=True,
                                       density_or_frequency='density', with_facilities=False, cmap='cmr.freeze_r', fontsize=16, rotation=50):
    datadir = sp.datadir

    state_location = 'Washington'
    location = 'seattle_metro'
    country_location = 'usa'

    # popdict = {}
    options_args = {'use_microstructure': True}
    network_distr_args = {'Npop': int(n)}

    population = sp.make_population(n, generate=True, with_facilities=with_facilities)

    # contacts = sp.make_contacts(popdict, state_location=state_location, location=location, options_args=options_args,
    #                             network_distr_args=network_distr_args)

    age_brackets = sp.get_census_age_brackets(datadir, state_location=state_location, country_location=country_location)
    age_by_brackets_dic = sp.get_age_by_brackets_dic(age_brackets)

    ages = []
    # if setting_code == 'LTCF':
    #     ltcf_ages = []

    for uid in population:
        ages.append(population[uid]['age'])
        # if setting_code == 'LTCF':
        #     if population[uid]['snf_res'] or population[uid]['snf_staff']:
        #         ltcf_ages.append(population[uid]['age'])

    age_count = Counter(ages)
    aggregate_age_count = sp.get_aggregate_ages(age_count, age_by_brackets_dic)

    # if setting_code == 'LTCF':
    #     ltcf_age_count = Counter(ltcf_ages)
    #     aggregate_ltcf_age_count = sp.get_aggregate_ages(ltcf_age_count, age_by_brackets_dic)

    matrix = sp.calculate_contact_matrix(population, density_or_frequency, setting_code)

    # if setting_code == 'LTCF':
    #     fig = sp.plot_contact_frequency(matrix, ltcf_age_count, aggregate_ltcf_age_count, age_brackets, age_by_brackets_dic,
    #                                     setting_code, density_or_frequency, logcolors_flag, aggregate_flag, cmap, fontsize, rotation)
    # else:
    #     fig = sp.plot_contact_frequency(matrix, age_count, aggregate_age_count, age_brackets, age_by_brackets_dic,
    #                                     setting_code, density_or_frequency, logcolors_flag, aggregate_flag, cmap, fontsize, rotation)

    fig = sp.plot_contact_frequency(matrix, age_count, aggregate_age_count, age_brackets, age_by_brackets_dic,
                                    setting_code, density_or_frequency, logcolors_flag, aggregate_flag, cmap, fontsize, rotation)



    return fig


def test_plot_generated_trimmed_contact_matrix(setting_code='H', n=5000, aggregate_flag=True, logcolors_flag=True,
                                               density_or_frequency='density', with_facilities=False, cmap='cmr.freeze_r', fontsize=16, rotation=50):
    datadir = sp.datadir

    state_location = 'Washington'
    location = 'seattle_metro'
    country_location = 'usa'

    # popdict = {}

    options_args = {'use_microstructure': True}
    network_distr_args = {'Npop': int(n)}
    # contacts = sp.make_contacts(popdict, state_location=state_location, location=location, options_args=options_args,
    #                             network_distr_args=network_distr_args)
    # contacts = sp.trim_contacts(contacts, trimmed_size_dic=None, use_clusters=False)

    population = sp.make_population(n, generate=True, with_facilities=with_facilities)

    age_brackets = sp.get_census_age_brackets(datadir, state_location=state_location, country_location=country_location)
    age_by_brackets_dic = sp.get_age_by_brackets_dic(age_brackets)

    ages = []
    for uid in population:
        ages.append(population[uid]['age'])

    age_count = Counter(ages)
    aggregate_age_count = sp.get_aggregate_ages(age_count, age_by_brackets_dic)

    matrix = sp.calculate_contact_matrix(population, density_or_frequency, setting_code)

    fig = sp.plot_contact_frequency(matrix, age_count, aggregate_age_count, age_brackets, age_by_brackets_dic,
                                    setting_code, density_or_frequency, logcolors_flag, aggregate_flag, cmap, fontsize, rotation)

    return fig


if __name__ == '__main__':

    datadir = sp.datadir

    n = int(22500)

    state_location = 'Washington'
    location = 'seattle_metro'
    country_location = 'usa'

    # setting_code = 'H'
    # setting_code = 'S'
    # setting_code = 'W'
    setting_code = 'LTCF'

    aggregate_flag = True
    # aggregate_flag = False
    logcolors_flag = True
    # logcolors_flag = False

    density_or_frequency = 'density'
    density_or_frequency = 'frequency'

    with_facilities = True
    # with_facilities = False

    # some plotting styles
    cmap = 'cmr.freeze_r'
    fontsize = 26
    rotation = 90

    do_save = True
    # do_save = False

    do_trimmed = True
    # do_trimmed = False

    if setting_code in ['S', 'W']:
        if do_trimmed:
            fig = test_plot_generated_trimmed_contact_matrix(setting_code, n, aggregate_flag, logcolors_flag, density_or_frequency, with_facilities, cmap, fontsize, rotation)
        else:
            fig = test_plot_generated_contact_matrix(setting_code, n, aggregate_flag, logcolors_flag, density_or_frequency, with_facilities, cmap, fontsize, rotation)

    elif setting_code in ['H', 'LTCF']:
        fig = test_plot_generated_contact_matrix(setting_code, n, aggregate_flag, logcolors_flag, density_or_frequency, with_facilities, cmap, fontsize, rotation)

    if do_save:
        fig_path = datadir.replace('data', 'figures')
        os.makedirs(fig_path, exist_ok=True)

        if setting_code in ['S', 'W']:
            if do_trimmed:
                if aggregate_flag:
                    fig_path = os.path.join(fig_path, 'contact_matrices_152_countries', country_location,
                                            state_location, location + '_npop_' + str(n) + '_' + density_or_frequency + '_close_contact_matrix_setting_' + setting_code + '_aggregate_age_brackets.pdf')
                else:
                    fig_path = os.path.join(fig_path, 'contact_matrices_152_countries', country_location,
                                            state_location, location + '_npop_' + str(n) + '_' + density_or_frequency + '_close_contact_matrix_setting_' + setting_code + '.pdf')
            else:
                if aggregate_flag:
                    fig_path = os.path.join(fig_path, 'contact_matrices_152_countries', country_location,
                                            state_location, location + '_npop_' + str(n) + '_' + density_or_frequency + '_contact_matrix_setting_' + setting_code + '_aggregate_age_brackets.pdf')
                else:
                    fig_path = os.path.join(fig_path, 'contact_matrices_152_countries', country_location,
                                            state_location, location + '_npop_' + str(n) + '_' + density_or_frequency + '_contact_matrix_setting_' + setting_code + '.pdf')

        elif setting_code in ['H', 'LTCF']:
            if aggregate_flag:
                fig_path = os.path.join(fig_path, 'contact_matrices_152_countries', country_location, state_location,
                                        location + '_npop_' + str(n) + '_' + density_or_frequency + '_contact_matrix_setting_' + setting_code + '_aggregate_age_brackets.pdf')
            else:
                fig_path = os.path.join(fig_path, 'contact_matrices_152_countries', country_location, state_location,
                                        location + '_npop_' + str(n) + '_' + density_or_frequency + '_contact_matrix_setting_' + setting_code + '.pdf')

        fig.savefig(fig_path, format='pdf')
        fig.savefig(fig_path.replace('pdf', 'png'), format='png')
        fig.savefig(fig_path.replace('pdf', 'svg'), format='svg')
    plt.show()
