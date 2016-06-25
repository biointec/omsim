#ifndef ENZYMEPANEL_HPP
#define ENZYMEPANEL_HPP

#include <map>

#include <wx/wx.h>

#include "tinyxml2.h"

struct enzyme {
        wxString id;
        wxString pattern;
        wxString label;
        wxString fn;
        wxString fp;
        
        enzyme(){}
        enzyme(wxString &id_, wxString &pattern_, wxString &label_, wxString &fn_, wxString &fp_)
              : id(id_), pattern(pattern_), label(label_), fn(fn_), fp(fp_)
        {
                
        }
};

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
                
                void parseXML();
                
                wxCheckListBox *m_clb;
                wxButton *m_importb;
                wxButton *m_exportb;
                wxButton *m_newb;
                wxButton *m_clearb;
                wxButton *m_deleteb;
};

enum {
        wxID_IMPORT = wxID_HIGHEST + 1,
        wxID_EXPORT = wxID_HIGHEST + 2
};

#endif
