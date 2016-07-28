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
                if (val_ != wxString()) {
                        val = val_;
                }
                if (str_ != wxString()) {
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
        
        void set(wxString const &tag, wxString const &val = wxString(), wxString const &str = wxString()) {
                auto pos = indices.find(tag);
                if (pos == indices.end()){
                        indices[tag] = entries.size();
                        entries.push_back(configuration_entry(tag, val, str));
                } else {
                        auto s = str;
                        if (s == wxString()) {
                                s = entries[indices[tag]].str;
                        }
                        entries[indices[tag]] = configuration_entry(tag, val, s);
                }
        }
        
        wxString get(wxString const &tag) {
                return entries[indices[tag]].val;
        }
        
        configuration(){
                circular = false;
                
                set(wxT("name"), wxT("Unnamed"), wxT("Name"));
                set(wxT("prefix"), wxT("omsim_output"), wxT("Prefix"));
                set(wxT("byte_prefix"), wxT("omsim"), wxT("Byte Prefix"));

                set(wxT("coverage"), wxT("0"), wxT("Minimal Coverage"));
                set(wxT("chips"), wxT("1"), wxT("Chip Count"));
                set(wxT("scans_per_chip"), wxT("30"), wxT("Scans Per Chip"));
                set(wxT("scan_size"), wxT("1500"), wxT("Scan Size (Megabase)"));

                set(wxT("avg_mol_len"), wxT("90000"), wxT("Molecule Length: Mean"));
                set(wxT("sd_mol_len"), wxT("85000"), wxT("Molecule Length: Standard Deviation"));
                set(wxT("min_mol_len"), wxT("1"), wxT("Molecule Length: Minimum"));
                set(wxT("max_mol_len"), wxT("2500000"), wxT("Molecule Length: Maximum"));
                set(wxT("min_nicks"), wxT("1"), wxT("Minimal Number of Nicks"));

                set(wxT("label_mu"), wxT("1500"), wxT("Label Merge: Mean"));
                set(wxT("label_treshold"), wxT("500"), wxT("Label Merge: Treshold"));
                set(wxT("label_factor"), wxT("100"), wxT("Label Merge: Factor"));
                set(wxT("nick_sd"), wxT("50"), wxT("Label position: Standard Deviation"));

                set(wxT("fragile_same"), wxT("50"), wxT("Fragile Distance: Same Strand Mean"));
                set(wxT("fragile_opposite"), wxT("150"), wxT("Fragile Distance: Opposite Strand Mean"));
                set(wxT("fragile_treshold"), wxT("25"), wxT("Fragile Distance: Treshold"));
                set(wxT("fragile_factor"), wxT("3"), wxT("Fragile Distance: Factor"));

                set(wxT("chimera_rate"), wxT("0.01"), wxT("Chimera Rate"));
                set(wxT("chimera_mu"), wxT("1500"), wxT("Chimera Distance: Mean"));
                set(wxT("chimera_sigma"), wxT("500"), wxT("Chimera Distance: Standard Deviation"));
                
                set(wxT("stretch_factor"), wxT("0.85"), wxT("Stretch Factor: Mean"));
                set(wxT("stretch_chip_sd"), wxT("0.01"), wxT("Stretch Factor: Chip Standard Deviation"));
                set(wxT("stretch_scan_sd"), wxT("0.001"), wxT("Stretch Factor: Scan Standard Deviation"));
                
                set(wxT("molecule_AI_mu"), wxT("0.3"), wxT("Molecule AI: Mean"));
                set(wxT("molecule_AI_sd"), wxT("0.2"), wxT("Molecule AI: Standard Deviation"));
                set(wxT("label_AI_mu"), wxT("0.07"), wxT("Label AI: Mean"));
                set(wxT("label_AI_sd"), wxT("0.04"), wxT("Label AI: Standard Deviation"));
                set(wxT("molecule_SNR_mu"), wxT("15.0"), wxT("Molecule SNR: Mean"));
                set(wxT("molecule_SNR_sd"), wxT("75.0"), wxT("Molecule SNR: Standard Deviation"));
                set(wxT("label_snr_filter_type"), wxT("Static"), wxT("Label SNR: Filter Type"));
                set(wxT("min_label_SNR"), wxT("0.0"), wxT("Label SNR: Minimum"));
                set(wxT("label_SNR_mu"), wxT("14.0"), wxT("Label SNR: Mean"));
                set(wxT("label_SNR_sd"), wxT("11.0"), wxT("Label SNR: Standard Deviation"));

                set(wxT("sim_batch_size"), wxT("100000"), wxT("Simulation Batch Size"));
                set(wxT("seed"), wxString(), wxT("PRNG Seed"));
        };
};

#endif
