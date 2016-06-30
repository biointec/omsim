#ifndef ENZYMEPANEL_HPP
#define ENZYMEPANEL_HPP

#include <map>

#include <wx/wx.h>

#include "tinyxml2.h"

#include "EnzymeDialog.hpp"

#include "configuration.hpp"

class EnzymePanel : public wxPanel
{
        private:
                int count;
                std::map<wxString, configuration> &configurations;
                std::map<wxString, enzyme> &enzymes;
                tinyxml2::XMLDocument *doc;
        public:
                EnzymePanel(wxWindow *parent, wxListBox * lb, std::map<wxString, configuration> &configurations_, std::map<wxString, enzyme> &enzymes_);
                void OnImport(wxCommandEvent& event);
                void OnExport(wxCommandEvent& event);
                void OnNew(wxCommandEvent& event);
                void OnClear(wxCommandEvent& event);
                void OnDelete(wxCommandEvent& event);
                void OnEnzDblClick(wxCommandEvent& event);
                
                void addXML(wxString const &xml);
                void parseXML();
                void updateXML();
                
                void update();
                
                wxListBox *m_lb;
                wxButton *m_importb;
                wxButton *m_exportb;
                wxButton *m_newb;
                wxButton *m_clearb;
                wxButton *m_deleteb;
                
                std::map<wxString, enzyme> get_enzymes() {return enzymes;}
};

enum {
        wxID_EIMPORT = wxID_HIGHEST + 1,
        wxID_EEXPORT = wxID_HIGHEST + 2
};

#endif
