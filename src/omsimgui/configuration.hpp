#ifndef CONFIGURATION_HPP
#define CONFIGURATION_HPP

#include <vector>
#include <map>

#include "enzyme.hpp"

struct configuration {
        bool circular;
        
        wxString name;
        wxString prefix;
        wxString byte_prefix;
        wxString coverage;
        wxString chips;
        wxString scans_per_chip;
        wxString scan_size;
        wxString avg_mol_len;
        wxString sd_mol_len;
        wxString min_mol_len;
        wxString max_mol_len;
        wxString min_nicks;
        wxString label_snr_filter_type;
        wxString min_label_SNR;
        wxString nick_sd;
        wxString fragile_same;
        wxString fragile_opposite;
        wxString fragile_treshold;
        wxString fragile_factor;
        wxString label_mu;
        wxString label_treshold;
        wxString label_factor;
        wxString chimera_rate;
        wxString chimera_mu;
        wxString chimera_sigma;
        wxString stretch_factor;
        wxString stretch_chip_sd;
        wxString stretch_scan_sd;
        wxString molecule_AI_mu;
        wxString molecule_AI_sd;
        wxString label_AI_mu;
        wxString label_AI_sd;
        wxString molecule_SNR_mu;
        wxString molecule_SNR_sd;
        wxString label_SNR_mu;
        wxString label_SNR_sd;
        wxString sim_batch_size;
        wxString seed;
        
        wxString enzyme_xml;
        
        std::vector<wxString> files;
        std::map<wxString, enzyme> enzymes;
        std::vector<wxString> labels;
        
        configuration(){
                circular = false;
                
                name = "Unnamed";
                prefix = "omsim_output";
                byte_prefix = "omsim";
                coverage = "0";
                chips = "1";
                scans_per_chip = "30";
                scan_size = "1500";
                avg_mol_len = "90000";
                sd_mol_len = "95000";
                min_mol_len = "1";
                max_mol_len = "2500000";
                min_nicks = "1";
                label_snr_filter_type = "Static";
                min_label_SNR = "0.0";
                nick_sd = "50";
                fragile_same = "50";
                fragile_opposite = "150";
                fragile_treshold = "25";
                fragile_factor = "3";
                label_mu = "1500";
                label_treshold = "500";
                label_factor = "100";
                chimera_rate = "0.01";
                chimera_mu = "1500";
                chimera_sigma = "500";
                stretch_factor = ".85";
                stretch_chip_sd = "0.01";
                stretch_scan_sd = "0.001";
                molecule_AI_mu = "0.3";
                molecule_AI_sd = "0.2";
                label_AI_mu = "0.07";
                label_AI_sd = "0.04";
                molecule_SNR_mu = "15.0";
                molecule_SNR_sd = "75.0";
                label_SNR_mu = "14.0";
                label_SNR_sd = "11.0";
                sim_batch_size = "100000";
                seed = "";
        };
};

#endif
