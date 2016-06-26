#ifndef ENZYMEPANEL_HPP
#define ENZYMEPANEL_HPP

#include <map>

#include <wx/wx.h>

#include "tinyxml2.h"

#include "EnzymeDialog.hpp"

class EnzymePanel : public wxPanel
{
        private:
                int count;
                std::map<wxString, enzyme> enzymes;
                tinyxml2::XMLDocument *doc;
        public:
                EnzymePanel(wxPanel *parent, wxCheckListBox * clb);
                void OnImport(wxCommandEvent& event);
                void OnExport(wxCommandEvent& event);
                void OnNew(wxCommandEvent& event);
                void OnClear(wxCommandEvent& event);
                void OnDelete(wxCommandEvent& event);
                void OnEnzDblClick(wxCommandEvent& event);
                
                void parseXML();
                void updateXML();
                
                wxCheckListBox *m_clb;
                wxButton *m_importb;
                wxButton *m_exportb;
                wxButton *m_newb;
                wxButton *m_clearb;
                wxButton *m_deleteb;
                
                std::map<wxString, enzyme> get_enzymes() {return enzymes;}
};

enum {
        wxID_IMPORT = wxID_HIGHEST + 1,
        wxID_EXPORT = wxID_HIGHEST + 2
};

#endif
