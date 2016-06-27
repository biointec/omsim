#ifndef CONFIGURATION_HPP
#define CONFIGURATION_HPP

#include <vector>
#include <map>

#include "enzyme.hpp"

struct configuration {
        wxString name;
        wxString prefix;
        bool circular;
        wxString coverage;
        wxString chips;
        wxString scans_per_chip;
        wxString scan_size;
        wxString avg_mol_len;
        wxString sd_mol_len;
        wxString fragile_correction;
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
        wxString sim_batch_size;
        wxString seed;
        
        std::vector<wxString> files;
        std::map<wxString, enzyme> enzymes;
        std::vector<wxString> labels;
        
        wxString enzymeFile;
        
        configuration(){
                circular = false;
        };
};

#endif
