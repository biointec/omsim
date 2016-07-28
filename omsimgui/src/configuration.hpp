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
                
                set("name", "Unnamed", "Name");
                set("prefix", "omsim_output", "Prefix");
                set("byte_prefix", "omsim", "Byte Prefix");

                set("coverage", "0", "Minimal Coverage");
                set("chips", "1", "Chip Count");
                set("scans_per_chip", "30", "Scans Per Chip");
                set("scan_size", "1500", "Scan Size (Megabase)");

                set("avg_mol_len", "90000", "Molecule Length: Mean");
                set("sd_mol_len", "85000", "Molecule Length: Standard Deviation");
                set("min_mol_len", "1", "Molecule Length: Minimum");
                set("max_mol_len", "2500000", "Molecule Length: Maximum");
                set("min_nicks", "1", "Minimal Number of Nicks");

                set("label_mu", "1500", "Label Merge: Mean");
                set("label_treshold", "500", "Label Merge: Treshold");
                set("label_factor", "100", "Label Merge: Factor");
                set("nick_sd", "50", "Label position: Standard Deviation");

                set("fragile_same", "50", "Fragile Distance: Same Strand Mean");
                set("fragile_opposite", "150", "Fragile Distance: Opposite Strand Mean");
                set("fragile_treshold", "25", "Fragile Distance: Treshold");
                set("fragile_factor", "3", "Fragile Distance: Factor");

                set("chimera_rate", "0.01", "Chimera Rate");
                set("chimera_mu", "1500", "Chimera Distance: Mean");
                set("chimera_sigma", "500", "Chimera Distance: Standard Deviation");
                
                set("stretch_factor", ".85", "Stretch Factor: Mean");
                set("stretch_chip_sd", "0.01", "Stretch Factor: Chip Standard Deviation");
                set("stretch_scan_sd", "0.001", "Stretch Factor: Scan Standard Deviation");
                
                set("molecule_AI_mu", "0.3", "Molecule AI: Mean");
                set("molecule_AI_sd", "0.2", "Molecule AI: Standard Deviation");
                set("label_AI_mu", "0.07", "Label AI: Mean");
                set("label_AI_sd", "0.04", "Label AI: Standard Deviation");
                set("molecule_SNR_mu", "15.0", "Molecule SNR: Mean");
                set("molecule_SNR_sd", "75.0", "Molecule SNR: Standard Deviation");
                set("label_snr_filter_type", "Static", "Label SNR: Filter Type");
                set("min_label_SNR", "0.0", "Label SNR: Minimum");
                set("label_SNR_mu", "14.0", "Label SNR: Mean");
                set("label_SNR_sd", "11.0", "Label SNR: Standard Deviation");

                set("sim_batch_size", "100000", "Simulation Batch Size");
                set("seed", "", "PRNG Seed");
        };
};

#endif
