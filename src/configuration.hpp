#ifndef CONFIGURATION_HPP
#define CONFIGURATION_HPP

#include <vector>
#include <map>

#include "enzyme.hpp"

struct configuration_entry {
        wxString tag;
        wxString val;
        wxString str;
        configuration_entry() {}
        configuration_entry(wxString const &tag_, wxString const &val_, wxString const &str_) {
                tag = tag_;
                if (val_ != "") {
                        val = val_;
                }
                if (str_ != "") {
                        str = str_;
                }
        }
};

struct configuration {
        bool circular;
        
        wxString name;
        
        std::vector<configuration_entry> entries;
        std::map<wxString, int> indices;
        
        wxString enzyme_xml;
        
        std::vector<wxString> files;
        std::map<wxString, enzyme> enzymes;
        std::vector<wxString> labels;
        
        void set(wxString const &tag, wxString const &val = "", wxString const &str = "") {
                auto pos = indices.find(tag);
                if (pos == indices.end()){
                        indices[tag] = entries.size();
                        entries.push_back(configuration_entry(tag, val, str));
                } else {
                        entries[indices[tag]] = configuration_entry(tag, val, str);
                }
        }
        
        wxString get(wxString const &tag) {
                return entries[indices[tag]].val;
        }
        
        configuration(){
                circular = false;
                
                set("name", "Unnamed", "name");
                set("prefix", "omsim_output", "prefix");
                set("byte_prefix", "omsim", "byte_prefix");
                set("coverage", "0", "coverage");
                set("chips", "1", "chips");
                set("scans_per_chip", "30", "scans_per_chip");
                set("scan_size", "1500", "scan_size");
                set("avg_mol_len", "90000", "avg_mol_len");
                set("sd_mol_len", "95000", "sd_mol_len");
                set("min_mol_len", "1", "min_mol_len");
                set("max_mol_len", "2500000", "max_mol_len");
                set("min_nicks", "1", "min_nicks");
                set("label_snr_filter_type", "Static", "label_snr_filter_type");
                set("min_label_SNR", "0.0", "min_label_SNR");
                set("nick_sd", "50", "nick_sd");
                set("fragile_same", "50", "fragile_same");
                set("fragile_opposite", "150", "fragile_opposite");
                set("fragile_treshold", "25", "fragile_treshold");
                set("fragile_factor", "3", "fragile_factor");
                set("label_mu", "1500", "label_mu");
                set("label_treshold", "500", "label_treshold");
                set("label_factor", "100", "label_factor");
                set("chimera_rate", "0.01", "chimera_rate");
                set("chimera_mu", "1500", "chimera_mu");
                set("chimera_sigma", "500", "chimera_sigma");
                set("stretch_factor", ".85", "stretch_factor");
                set("stretch_chip_sd", "0.01", "stretch_chip_sd");
                set("stretch_scan_sd", "0.001", "stretch_scan_sd");
                set("molecule_AI_mu", "0.3", "molecule_AI_mu");
                set("molecule_AI_sd", "0.2", "molecule_AI_sd");
                set("label_AI_mu", "0.07", "label_AI_mu");
                set("label_AI_sd", "0.04", "label_AI_sd");
                set("molecule_SNR_mu", "15.0", "molecule_SNR_mu");
                set("molecule_SNR_sd", "75.0", "molecule_SNR_sd");
                set("label_SNR_mu", "14.0", "label_SNR_mu");
                set("label_SNR_sd", "11.0", "label_SNR_sd");
                set("sim_batch_size", "100000", "sim_batch_size");
                set("seed", "", "seed");
        };
};

#endif
