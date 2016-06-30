#include "ConfigurationPanel.hpp"
#include <wx/textdlg.h>

#include "Notebook.hpp"

#include <vector>
#include "MainFrame.hpp"

ConfigurationPanel::ConfigurationPanel(wxPanel * parent, wxCheckListBox * clb, std::map<wxString, configuration> &configurations_, std::map<wxString, enzyme> &enzymes_)
      : wxPanel(parent, wxID_ANY), configurations(configurations_), enzymes(enzymes_)
{
        doc = new tinyxml2::XMLDocument();
        wxBoxSizer *vbox = new wxBoxSizer(wxVERTICAL);
        m_clb = clb;
        m_importb = new wxButton(this, wxID_CIMPORT, wxT("Import file"));
        m_exportb = new wxButton(this, wxID_CEXPORT, wxT("Export file"));
        m_newb = new wxButton(this, wxID_NEW, wxT("Add configuration"));
        m_deleteb = new wxButton(this, wxID_DELETE, wxT("Delete configuration"));
        m_clearb = new wxButton(this, wxID_CLEAR, wxT("Clear"));
        Connect(wxID_CIMPORT, wxEVT_COMMAND_BUTTON_CLICKED, 
                wxCommandEventHandler(ConfigurationPanel::OnImport));
        Connect(wxID_CEXPORT, wxEVT_COMMAND_BUTTON_CLICKED, 
                wxCommandEventHandler(ConfigurationPanel::OnExport));
        Connect(wxID_NEW, wxEVT_COMMAND_BUTTON_CLICKED, 
                wxCommandEventHandler(ConfigurationPanel::OnNew));
        Connect(wxID_CLEAR, wxEVT_COMMAND_BUTTON_CLICKED, 
                wxCommandEventHandler(ConfigurationPanel::OnClear));
        Connect(wxID_DELETE, wxEVT_COMMAND_BUTTON_CLICKED, 
                wxCommandEventHandler(ConfigurationPanel::OnDelete));
        
        vbox->Add(-1, 20);
        vbox->Add(m_importb, 1, wxEXPAND | wxRIGHT, 10);
        vbox->Add(m_exportb, 1, wxEXPAND | wxRIGHT, 10);
        vbox->Add(m_newb, 1, wxEXPAND | wxRIGHT, 10);
        vbox->Add(m_deleteb, 1, wxEXPAND | wxRIGHT, 10);
        vbox->Add(m_clearb, 1, wxEXPAND | wxRIGHT, 10);
        vbox->Add(-1, 5);
        
        SetSizerAndFit(vbox);
}

void ConfigurationPanel::parseXML() {
        //configurations.clear();
        m_clb->Clear();
        auto child = doc->FirstChildElement()->FirstChildElement();
        count = 0;
        while (child != NULL) {
                count += 1;
                
                configuration c;
                /*
                        Required parameters
                */
                int const tag_count = 36;
                wxString tags [tag_count] = {"name", "prefix", "coverage", "chips", "scans_per_chip", "scan_size", "avg_mol_len", "sd_mol_len", "fragile_correction", "min_mol_len", "max_mol_len", "min_nicks", "label_snr_filter_type", "min_label_SNR", "nick_sd", "fragile_same", "fragile_opposite", "fragile_treshold", "fragile_factor", "label_mu", "label_treshold", "label_factor", "chimera_rate", "chimera_mu", "chimera_sigma", "stretch_factor", "stretch_chip_sd", "stretch_scan_sd", "molecule_AI_mu", "molecule_AI_sd", "label_AI_mu", "label_AI_sd", "molecule_SNR_mu", "molecule_SNR_sd", "sim_batch_size", "seed"};
                wxString vals [tag_count] = {c.name, c.prefix, c.coverage, c.chips, c.scans_per_chip, c.scan_size, c.avg_mol_len, c.sd_mol_len, c.fragile_correction, c.min_mol_len, c.max_mol_len, c.min_nicks, c.label_snr_filter_type, c.min_label_SNR, c.nick_sd, c.fragile_same, c.fragile_opposite, c.fragile_treshold, c.fragile_factor, c.label_mu, c.label_treshold, c.label_factor, c.chimera_rate, c.chimera_mu, c.chimera_sigma, c.stretch_factor, c.stretch_chip_sd, c.stretch_scan_sd, c.molecule_AI_mu, c.molecule_AI_sd, c.label_AI_mu, c.label_AI_sd, c.molecule_SNR_mu, c.molecule_SNR_sd, c.sim_batch_size, c.seed};
                for (auto i = 0; i < tag_count; ++i) {
                        if (child->FirstChildElement(tags[i]) != NULL) {
                                vals[i] = child->FirstChildElement(tags[i])->GetText();
                        }
                }
                
                if (child->FirstChildElement("files") != NULL && 
                        child->FirstChildElement("files")->FirstChildElement("file") != NULL)
                {
                        auto file = child->FirstChildElement("files")->FirstChildElement("file");
                        while (file != NULL) {
                                c.files.push_back(file->GetText());
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
                                c.enzymes[vals[0]] = enzyme(vals[0], vals[1], vals[2], vals[3], vals[4]);
                                enzymeElement = enzymeElement->NextSiblingElement("enzyme");
                        }
                }
                
                if (child->FirstChildElement("circular") != NULL) {
                        c.circular = true;
                }
                
                /*
                        Optional parameters
                */
                
                /*
                        Store configuration
                */
                configurations[c.name] = c;
                m_clb->Append(c.name);
                
                child = child->NextSiblingElement();
        }
}

void ConfigurationPanel::updateParent() {
        ((MainFrame *) GetGrandParent())->update();
}

void ConfigurationPanel::update() {
        //
}

void ConfigurationPanel::updateXML() {
        if (doc->FirstChildElement() != NULL) {
                doc->DeleteNode(doc->FirstChildElement());
        }
        auto * top = doc->NewElement("simulation");
        for (auto kv : configurations) {
                auto c = kv.second;
                auto *child = doc->NewElement("input");
                
                auto *files = doc->NewElement("files");
                for (auto f : c.files) {
                        auto *file = doc->NewElement("file");
                        auto *fileText = doc->NewText(f);
                        file->LinkEndChild(fileText);
                        files->LinkEndChild(file);
                }
                child->LinkEndChild(files);
                
                if (c.circular) {
                        auto *circular = doc->NewElement("circular");
                        child->LinkEndChild(circular);
                }
                
                auto *enzymesElement = doc->NewElement("enzymes");
                if (c.enzymeFile != "") {
                        auto *enzymeFile = doc->NewElement("file");
                        auto enzymeFileText = doc->NewText(c.enzymeFile);
                        enzymeFile->LinkEndChild(enzymeFileText);
                        enzymesElement->LinkEndChild(enzymeFile);
                }
                for (auto kv : c.enzymes) {
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
                child->LinkEndChild(enzymesElement);
                
                int const tag_count = 36;
                wxString tags [tag_count] = {"name", "prefix", "coverage", "chips", "scans_per_chip", "scan_size", "avg_mol_len", "sd_mol_len", "fragile_correction", "min_mol_len", "max_mol_len", "min_nicks", "label_snr_filter_type", "min_label_SNR", "nick_sd", "fragile_same", "fragile_opposite", "fragile_treshold", "fragile_factor", "label_mu", "label_treshold", "label_factor", "chimera_rate", "chimera_mu", "chimera_sigma", "stretch_factor", "stretch_chip_sd", "stretch_scan_sd", "molecule_AI_mu", "molecule_AI_sd", "label_AI_mu", "label_AI_sd", "molecule_SNR_mu", "molecule_SNR_sd", "sim_batch_size", "seed"};
                wxString vals [tag_count] = {c.name, c.prefix, c.coverage, c.chips, c.scans_per_chip, c.scan_size, c.avg_mol_len, c.sd_mol_len, c.fragile_correction, c.min_mol_len, c.max_mol_len, c.min_nicks, c.label_snr_filter_type, c.min_label_SNR, c.nick_sd, c.fragile_same, c.fragile_opposite, c.fragile_treshold, c.fragile_factor, c.label_mu, c.label_treshold, c.label_factor, c.chimera_rate, c.chimera_mu, c.chimera_sigma, c.stretch_factor, c.stretch_chip_sd, c.stretch_scan_sd, c.molecule_AI_mu, c.molecule_AI_sd, c.label_AI_mu, c.label_AI_sd, c.molecule_SNR_mu, c.molecule_SNR_sd, c.sim_batch_size, c.seed};
                for (auto i = 0; i < tag_count; ++i) {
                        auto tag = tags[i];
                        auto val = vals[i];
                        if (val != "") {
                                auto tagChild = doc->NewElement(tag);
                                auto valChild = doc->NewText(val);
                                tagChild->LinkEndChild(valChild);
                                child->LinkEndChild(tagChild);
                        }
                }
                
                top->LinkEndChild(child);
        }
        doc->LinkEndChild(top);
}

void ConfigurationPanel::OnImport(wxCommandEvent& event) 
{
        wxFileDialog openDialog(this,
                _("Choose a file to open"), wxEmptyString, wxEmptyString,
                _("XML Files (*.xml)|*.xml"), wxFD_MULTIPLE);
        if (openDialog.ShowModal() == wxID_CANCEL) {
                return;
        } else {
                doc->LoadFile(openDialog.GetPath());
                parseXML();
        }
        updateParent();
}

void ConfigurationPanel::OnExport(wxCommandEvent& event) 
{
        wxFileDialog saveDialog(this,
                _("Save XML file"), wxEmptyString, wxEmptyString,
                _("XML files (*.xml)|*.xml"), wxFD_SAVE|wxFD_OVERWRITE_PROMPT);
        if (saveDialog.ShowModal() == wxID_CANCEL) {
                return;
        } else {
                updateXML();
                doc->SaveFile(saveDialog.GetPath());
        }
}

void ConfigurationPanel::OnNew(wxCommandEvent& event) 
{
        configuration c;
        Notebook dlg(this, wxID_ANY, _("Add configuration"), c, enzymes, wxDefaultPosition, wxSize(500, 700));
        if (dlg.ShowModal() == wxID_CANCEL) {
                return;
        } else {
                auto c = dlg.GetConfiguration();
                configurations[c.name] = c;
                m_clb->Append(c.name);
        }
        updateParent();
}

void ConfigurationPanel::OnClear(wxCommandEvent& event) 
{
        m_clb->Clear();
        configurations.clear();
}

void ConfigurationPanel::OnDelete(wxCommandEvent& event) 
{
        int sel = m_clb->GetSelection();
        if (sel != -1) {
                auto id = m_clb->GetString(sel);
                m_clb->Delete(sel);
                configurations.erase(id);
        }
}

void ConfigurationPanel::OnConfDblClick(wxCommandEvent& event)
{
        int sel = m_clb->GetSelection();
        if (sel != -1) {
                auto name = m_clb->GetString(sel);
                Notebook dlg(this, wxID_ANY, _("Edit configuration"), configurations[name], enzymes, wxDefaultPosition, wxSize(500, 700));
                if (dlg.ShowModal() == wxID_CANCEL) {
                        return;
                } else {
                        auto c = dlg.GetConfiguration();
                        configurations[c.name] = c;
                        m_clb->Delete(sel);
                        m_clb->Insert(c.name, sel);
                }
        }
        updateParent();
}
