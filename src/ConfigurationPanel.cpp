#include "ConfigurationPanel.hpp"
#include <wx/textdlg.h>

#include "Notebook.hpp"

#include <vector>

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
        vbox->Add(m_importb);
        vbox->Add(m_exportb);
        vbox->Add(m_newb);
        vbox->Add(m_deleteb);
        vbox->Add(m_clearb);
        vbox->Add(-1, 5);
        
        SetSizer(vbox);
}

void ConfigurationPanel::parseXML() {
        //configurations.clear();
        m_clb->Clear();
        auto child = doc->FirstChildElement("simulation")->FirstChildElement("input");
        count = 0;
        while (child != NULL) {
                count += 1;
                
                configuration c;
                c.name = child->FirstChildElement("name")->GetText();
                
                auto file = child->FirstChildElement("files")->FirstChildElement("file");
                while (file != NULL) {
                        c.files.push_back(file->GetText());
                        file = file->NextSiblingElement("file");
                }
                
                auto enzymeElement = child->FirstChildElement("enzymes")->FirstChildElement("enzyme");
                while (file != NULL) {
                        auto id = enzymeElement->FirstChildElement("id")->GetText();
                        auto label = enzymeElement->FirstChildElement("label")->GetText();
                        c.enzymes.push_back(enzyme(id, "", label, "", ""));
                        enzymeElement = enzymeElement->NextSiblingElement("enzyme");
                }
                
                if (child->FirstChildElement("circular") != NULL) {
                        c.circular = true;
                }
                
                configurations[c.name] = c;
                m_clb->Append(c.name);
                
                child = child->NextSiblingElement("input");
        }
}

void ConfigurationPanel::updateXML() {
        if (doc->FirstChildElement() != NULL) {
                doc->DeleteNode(doc->FirstChildElement());
        }
        auto * top = doc->NewElement("simulation");
        for (auto kv : configurations) {
                auto c = kv.second;
                auto *child = doc->NewElement("input");
                
                auto *name = doc->NewElement("name");
                auto *nameText = doc->NewText(c.name);
                name->LinkEndChild(nameText);
                child->LinkEndChild(name);
                
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
                
                auto *enzymes = doc->NewElement("enzymes");
                auto *enzymeFile = doc->NewElement("file");
                auto enzymeFileText = doc->NewText(c.enzymeFile);
                enzymeFile->LinkEndChild(enzymeFileText);
                enzymes->LinkEndChild(enzymeFile);
                for (auto e : c.enzymes) {
                        auto *enzyme = doc->NewElement("enzyme");
                        
                        auto *enzymeID = doc->NewElement("id");
                        auto enzymeIDText = doc->NewText(e.id);
                        enzymeID->LinkEndChild(enzymeIDText);
                        enzyme->LinkEndChild(enzymeID);
                        
                        auto *enzymeLabel = doc->NewElement("label");
                        auto enzymeLabelText = doc->NewText(e.label);
                        enzymeLabel->LinkEndChild(enzymeLabelText);
                        enzyme->LinkEndChild(enzymeLabel);
                        
                        enzymes->LinkEndChild(enzyme);
                }
                child->LinkEndChild(files);
                
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
        Notebook dlg(this, wxID_ANY, _("Add configuration"), c, enzymes, wxDefaultPosition, wxSize(700, 700));
        if (dlg.ShowModal() == wxID_CANCEL) {
                return;
        } else {
                auto c = dlg.GetConfiguration();
                configurations[c.name] = c;
                m_clb->Append(c.name);
        }
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
                Notebook dlg(this, wxID_ANY, _("Edit configuration"), configurations[name], enzymes, wxDefaultPosition, wxSize(700, 700));
                if (dlg.ShowModal() == wxID_CANCEL) {
                        return;
                } else {
                        auto c = dlg.GetConfiguration();
                        configurations[c.name] = c;
                        m_clb->Delete(sel);
                        m_clb->Insert(c.name, sel);
                }
        }
}
