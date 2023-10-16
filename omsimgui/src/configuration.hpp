/*
        Copyright (C) 2016 Giles Miclotte (giles.miclotte@ugent.be)
        This file is part of OMSim

        This program is free software; you can redistribute it and/or modify
        it under the terms of the GNU General Public License as published by
        the Free Software Foundation; either version 2 of the License, or
        (at your option) any later version.

        This program is distributed in the hope that it will be useful,
        but WITHOUT ANY WARRANTY; without even the implied warranty of
        MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
        GNU General Public License for more details.

        You should have received a copy of the GNU General Public License
        along with this program; if not, write to the
        Free Software Foundation, Inc.,
        59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
*/
#ifndef CONFIGURATION_HPP
#define CONFIGURATION_HPP

#include <vector>
#include <map>

#include "tinyxml2.h"

#include "enzyme.hpp"

enum ConfType{
        NAME,
        BASIC,
        ADVANCED,
        DEPRECATED
};

struct configuration_entry {
        wxString tag;
        wxString val;
        wxString str;
        ConfType type;
        configuration_entry() {}
        configuration_entry(wxString const &tag_, wxString const &val_, wxString const &str_, ConfType type_) {
                tag = tag_;
                if (val_ != wxString()) {
                        val = val_;
                }
                if (str_ != wxString()) {
                        str = str_;
                }
                type = type_;
        }
};

struct configuration {
        wxString xml;
        tinyxml2::XMLDocument *doc;
        
        bool circular;
        
        wxString name;
        
        std::vector<configuration_entry> entries;
        std::map<wxString, int> indices;
        
        wxString enzyme_xml;
        
        std::vector<wxString> files;
        std::map<wxString, enzyme> enzymes;
        std::vector<wxString> labels;
        
        void set(wxString const &tag, wxString const &val = wxString(), wxString const &str = wxString(), ConfType type = ADVANCED) {
                auto pos = indices.find(tag);
                if (pos == indices.end()){
                        indices[tag] = entries.size();
                        entries.push_back(configuration_entry(tag, val, str, type));
                } else {
                        auto s = str;
                        if (s == wxString()) {
                                s = entries[indices[tag]].str;
                        }
                        entries[indices[tag]] = configuration_entry(tag, val, s, type);
                }
        }
        
        wxString get(wxString const &tag) {
                return entries[indices[tag]].val;
        }
        
        configuration() {
                doc = new tinyxml2::XMLDocument();
                new_config();
        }
        
        void open_config(wxString xml_) {
                xml = xml_;
                doc->LoadFile(xml);
                parseXML();
        }
        
        void new_config() {
                xml = "";
                
                circular = false;
                
                set(wxT("name"), wxT("Unnamed"), wxT("Name"), NAME);
                set(wxT("prefix"), wxT("omsim_output"), wxT("Prefix"));
                set(wxT("byte_prefix"), wxT("omsim"), wxT("Byte Prefix"));

                set(wxT("coverage"), wxT("0"), wxT("Minimal Coverage"), DEPRECATED);
                set(wxT("chips"), wxT("1"), wxT("Chip Count"), BASIC);
                set(wxT("scans_per_chip"), wxT("30"), wxT("Scans Per Chip"));
                set(wxT("scan_size"), wxT("1500"), wxT("Scan Size (Megabase)"));

                set(wxT("avg_mol_len"), wxT("90000"), wxT("Molecule Length: Mean"), BASIC);
                set(wxT("sd_mol_len"), wxT("85000"), wxT("Molecule Length: Standard Deviation"), BASIC);
                set(wxT("min_mol_len"), wxT("1"), wxT("Molecule Length: Minimum"));
                set(wxT("max_mol_len"), wxT("2500000"), wxT("Molecule Length: Maximum"));
                set(wxT("min_nicks"), wxT("1"), wxT("Minimal Number of Nicks"));

                set(wxT("label_mu"), wxT("1500"), wxT("Label Merge: Mean"));
                set(wxT("label_threshold"), wxT("500"), wxT("Label Merge: Threshold"));
                set(wxT("label_factor"), wxT("100"), wxT("Label Merge: Factor"));
                set(wxT("nick_sd"), wxT("50"), wxT("Label position: Standard Deviation"));

                set(wxT("fragile_same"), wxT("50"), wxT("Fragile Distance: Same Strand Mean"));
                set(wxT("fragile_opposite"), wxT("150"), wxT("Fragile Distance: Opposite Strand Mean"));
                set(wxT("fragile_threshold"), wxT("25"), wxT("Fragile Distance: Threshold"));
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
                auto e = enzyme();
                enzymes[e.id] = e;
        };
        
        void parseXML() {
                auto child = doc->FirstChildElement()->FirstChildElement();
                if (child != NULL) {
                        /*
                                Required parameters
                        */
                        for (auto &entry : entries) {
                                auto &tag = entry.tag;
                                auto &val = entry.val;
                                if (child->FirstChildElement(tag) != NULL) {
                                        val = child->FirstChildElement(tag)->GetText();
                                }
                        }
                        
                        if (child->FirstChildElement("files") != NULL && 
                                child->FirstChildElement("files")->FirstChildElement("file") != NULL)
                        {
                                auto file = child->FirstChildElement("files")->FirstChildElement("file");
                                while (file != NULL) {
                                        files.push_back(file->GetText());
                                        file = file->NextSiblingElement("file");
                                }
                        }
                        
                        if (child->FirstChildElement("enzymes") != NULL &&
                                child->FirstChildElement("enzymes")->FirstChildElement("enzyme") != NULL)
                        {
                                auto enzymeElement = child->FirstChildElement("enzymes")->FirstChildElement("enzyme");
                                while (enzymeElement != NULL) {
                                        wxString tags [5] = {"id", "pattern", "label", "fn", "fp"};
                                        wxString vals [5] = {};
                                        for (auto i = 0; i < 5; ++i) {
                                                if (enzymeElement->FirstChildElement(tags[i]) != NULL) {
                                                        vals[i] = enzymeElement->FirstChildElement(tags[i])->GetText();
                                                }
                                        }
                                        enzymes[vals[0]] = enzyme(vals[0], vals[1], vals[2], vals[3], vals[4]);
                                        enzymeElement = enzymeElement->NextSiblingElement("enzyme");
                                }
                        }
                        
                        if (child->FirstChildElement("circular") != NULL) {
                                circular = true;
                        }
                }
        }
        
        void updateXML() {
                if (doc->FirstChildElement() != NULL) {
                        doc->DeleteNode(doc->FirstChildElement());
                }
                auto * top = doc->NewElement("simulation");
                auto *child = doc->NewElement("input");
                auto *filesElement = doc->NewElement("files");
                for (auto f : files) {
                        auto *file = doc->NewElement("file");
                        auto *fileText = doc->NewText(f);
                        file->LinkEndChild(fileText);
                        filesElement->LinkEndChild(file);
                }
                child->LinkEndChild(filesElement);
                if (circular) {
                        auto *circular = doc->NewElement("circular");
                        child->LinkEndChild(circular);
                }
                auto *enzymesElement = doc->NewElement("enzymes");
                for (auto kv : enzymes) {
                        if (kv.second.checked) {
                                auto e = enzymes[kv.first];
                                auto *enzymeElement = doc->NewElement("enzyme");
                                wxString tags [5] = {"id", "pattern", "label", "fn", "fp"};
                                wxString vals [5] = {e.id, e.pattern, e.label, e.fn, e.fp};
                                for (auto i = 0; i < 5; ++i) {
                                        auto enzymeChild = doc->NewElement(tags[i]);
                                        auto enzymeChildText = doc->NewText(vals[i]);
                                        enzymeChild->LinkEndChild(enzymeChildText);
                                        enzymeElement->LinkEndChild(enzymeChild);
                                }
                                enzymesElement->LinkEndChild(enzymeElement);
                        }
                }
                child->LinkEndChild(enzymesElement);
                for (auto &entry : entries) {
                        auto &tag = entry.tag;
                        auto &val = entry.val;
                        if (val != "") {
                                auto tagChild = doc->NewElement(tag);
                                auto valChild = doc->NewText(val);
                                tagChild->LinkEndChild(valChild);
                                child->LinkEndChild(tagChild);
                        }
                }
                top->LinkEndChild(child);
                doc->LinkEndChild(top);
        }
        
        void save() {
                save_as(xml);
        }
        
        void save_as(wxString const &path) {
                updateXML();
                doc->SaveFile(path);
        }
};      

#endif
