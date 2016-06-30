#ifndef CONFIGURATIONPANEL_HPP
#define CONFIGURATIONPANEL_HPP

#include <map>
#include <vector>

#include <wx/wx.h>

#include "tinyxml2.h"

#include "configuration.hpp"

class ConfigurationPanel : public wxPanel
{
        private:
                int count;
                std::map<wxString, configuration> &configurations;
                std::map<wxString, enzyme> &enzymes;
        public:
                ConfigurationPanel(wxWindow *parent, wxCheckListBox * clb, std::map<wxString, configuration> &configurations_, std::map<wxString, enzyme> &enzymes_);
                void OnImport(wxCommandEvent& event);
                void OnExport(wxCommandEvent& event);
                void OnNew(wxCommandEvent& event);
                void OnClear(wxCommandEvent& event);
                void OnDelete(wxCommandEvent& event);
                void OnConfDblClick(wxCommandEvent& event);
                
                void parseXML();
                void updateXML();
                
                void updateParent();
                void update();
                
                wxCheckListBox *m_clb;
                wxButton *m_importb;
                wxButton *m_exportb;
                wxButton *m_newb;
                wxButton *m_clearb;
                wxButton *m_deleteb;
                
                tinyxml2::XMLDocument *doc;
};

enum {
        wxID_CIMPORT = wxID_HIGHEST + 1,
        wxID_CEXPORT = wxID_HIGHEST + 2
};

#endif
