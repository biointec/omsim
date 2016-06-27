#include "EnzymePanel.hpp"
#include <wx/textdlg.h>

#include <vector>

EnzymePanel::EnzymePanel(wxPanel * parent, wxListBox * lb, std::map<wxString, configuration> &configurations_, std::map<wxString, enzyme> &enzymes_)
      : wxPanel(parent, wxID_ANY), configurations(configurations_), enzymes(enzymes_)
{
        doc = new tinyxml2::XMLDocument();
        wxBoxSizer *vbox = new wxBoxSizer(wxVERTICAL);
        m_lb = lb;
        m_importb = new wxButton(this, wxID_EIMPORT, wxT("Import file"));
        m_exportb = new wxButton(this, wxID_EEXPORT, wxT("Export file"));
        m_newb = new wxButton(this, wxID_NEW, wxT("Add enzyme"));
        m_deleteb = new wxButton(this, wxID_DELETE, wxT("Delete enzyme"));
        m_clearb = new wxButton(this, wxID_CLEAR, wxT("Clear"));
        Connect(wxID_EIMPORT, wxEVT_COMMAND_BUTTON_CLICKED, 
                wxCommandEventHandler(EnzymePanel::OnImport));
        Connect(wxID_EEXPORT, wxEVT_COMMAND_BUTTON_CLICKED, 
                wxCommandEventHandler(EnzymePanel::OnExport));
        Connect(wxID_NEW, wxEVT_COMMAND_BUTTON_CLICKED, 
                wxCommandEventHandler(EnzymePanel::OnNew));
        Connect(wxID_CLEAR, wxEVT_COMMAND_BUTTON_CLICKED, 
                wxCommandEventHandler(EnzymePanel::OnClear));
        Connect(wxID_DELETE, wxEVT_COMMAND_BUTTON_CLICKED, 
                wxCommandEventHandler(EnzymePanel::OnDelete));
        
        vbox->Add(-1, 20);
        vbox->Add(m_importb);
        vbox->Add(m_exportb);
        vbox->Add(m_newb);
        vbox->Add(m_deleteb);
        vbox->Add(m_clearb);
        vbox->Add(-1, 5);
        
        SetSizer(vbox);
}

void EnzymePanel::parseXML() {
        auto child = doc->FirstChildElement("enzymes")->FirstChildElement("enzyme");
        count = 0;
        while (child != NULL) {
                count += 1;
                wxString id = child->FirstChildElement("id")->GetText();
                wxString pattern = child->FirstChildElement("pattern")->GetText();
                wxString label = wxString("label_") + wxString::Format(wxT("%d"), (int) (count - 1));
                wxString fn = child->FirstChildElement("fn")->GetText();
                wxString fp = child->FirstChildElement("fp")->GetText();
                enzymes[id] = enzyme(id, pattern, label, fn, fp);
                child = child->NextSiblingElement("enzyme");
        }
        update();
}

void EnzymePanel::update() {
        m_lb->Clear();
        for (auto kv : enzymes) {
                m_lb->Append(kv.first);
        }
}

void EnzymePanel::updateXML() {
        if (doc->FirstChildElement() != NULL) {
                doc->DeleteNode(doc->FirstChildElement());
        }
        auto * top = doc->NewElement("enzymes");
        for (auto kv : enzymes) {
                auto e = kv.second;
                auto *child = doc->NewElement("enzyme");
                auto *id = doc->NewElement("id");
                auto *idText = doc->NewText(e.id);
                id->LinkEndChild(idText);
                child->LinkEndChild(id);
                auto *pattern = doc->NewElement("pattern");
                auto *patternText = doc->NewText(e.pattern);
                pattern->LinkEndChild(patternText);
                child->LinkEndChild(pattern);
                auto *fn = doc->NewElement("fn");
                auto *fnText = doc->NewText(e.fn);
                fn->LinkEndChild(fnText);
                child->LinkEndChild(fn);
                auto *fp = doc->NewElement("fp");
                auto *fpText = doc->NewText(e.fp);
                fp->LinkEndChild(fpText);
                child->LinkEndChild(fp);
                top->LinkEndChild(child);
        }
        doc->LinkEndChild(top);
}

void EnzymePanel::OnImport(wxCommandEvent& event) 
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

void EnzymePanel::OnExport(wxCommandEvent& event) 
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

void EnzymePanel::OnNew(wxCommandEvent& event) 
{
        EnzymeDialog dlg(this, wxID_ANY, _("Add enzyme"));
        if (dlg.ShowModal() == wxID_CANCEL) {
                return;
        } else {
                enzyme e = dlg.GetEnzyme();
                enzymes[e.id] = e;
                m_lb->Append(e.id);
        }
}

void EnzymePanel::OnClear(wxCommandEvent& event) 
{
        m_lb->Clear();
        enzymes.clear();
}

void EnzymePanel::OnDelete(wxCommandEvent& event) 
{
        int sel = m_lb->GetSelection();
        if (sel != -1) {
                wxString id = m_lb->GetString(sel);
                m_lb->Delete(sel);
                enzymes.erase(id);
        }
}

void EnzymePanel::OnEnzDblClick(wxCommandEvent& event)
{
        int sel = m_lb->GetSelection();
        if (sel != -1) {
                wxString id = m_lb->GetString(sel);
                EnzymeDialog dlg(this, wxID_ANY, _("Add enzyme"), enzymes[id]);
                if (dlg.ShowModal() == wxID_CANCEL) {
                        return;
                } else {
                        enzyme e = dlg.GetEnzyme();
                        enzymes[e.id] = e;
                        m_lb->Delete(sel);
                        m_lb->Insert(e.id, sel);
                }
        }
}
