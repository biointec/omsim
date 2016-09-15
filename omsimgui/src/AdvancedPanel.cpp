#include "AdvancedPanel.hpp"
#include "TagPanel.hpp"

#include <wx/scrolwin.h>


AdvancedPanel::AdvancedPanel(wxWindow *parent, wxWindowID id, configuration &c_)
      : wxPanel(parent, id), c(c_)
{
        wxBoxSizer *mainbox = new wxBoxSizer(wxHORIZONTAL);
        
        /*
                ctrl box
        */
        wxScrolledWindow *scrollbox = new wxScrolledWindow(this, wxID_ANY);
        
        wxBoxSizer *vbox = new wxBoxSizer(wxVERTICAL);
        
        for (auto &entry : c.entries) {
                auto &tag = entry.tag;
                auto &val = entry.val;
                auto &str = entry.str;
                tags.push_back(new TagPanel(scrollbox, vbox, tag, val, str));
        }
        
        scrollbox->SetSizerAndFit(vbox);
        scrollbox->FitInside();
        scrollbox->SetScrollRate(5, 5);
        /*
                close box
        */
        wxBoxSizer *closebox = new wxBoxSizer(wxVERTICAL);
        wxButton *ok = new wxButton(this, wxID_OK, wxT("Ok"));
        wxButton *cancel = new wxButton(this, wxID_CANCEL, wxT("Cancel"));
        closebox->Add(ok, 0, wxEXPAND | wxALIGN_CENTER);
        closebox->Add(cancel, 0, wxEXPAND | wxALIGN_CENTER);
        
        mainbox->Add(scrollbox, 0, wxEXPAND | wxALIGN_CENTER | wxALL, 5);
        mainbox->Add(closebox, 0, wxEXPAND | wxALIGN_CENTER | wxRIGHT | wxTOP | wxBOTTOM, 5);
        
        SetSizerAndFit(mainbox);
}

void AdvancedPanel::update(){
        for (auto tag : tags) {
                tag->update();
        }
}
