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
        };
};

#endif
