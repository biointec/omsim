#ifndef ENZYMEDIALOG_HPP
#define ENZYMEDIALOG_HPP

#include "wx.hpp"
#include <wx/dialog.h>

#include "enzyme.hpp"

class EnzymeDialog : public wxDialog
{
        private:
                wxTextCtrl *idCtrl;
                wxTextCtrl *patternCtrl;
                wxTextCtrl *fnCtrl;
                wxTextCtrl *fpCtrl;
                wxTextCtrl *labelCtrl;
                
                enzyme e;
        public:
                EnzymeDialog(wxWindow *parent, wxWindowID id, const wxString &title, enzyme const &e_=enzyme(wxString(), wxString(), wxString(), wxString(), wxString()), const wxPoint &pos=wxDefaultPosition, const wxSize &size=wxDefaultSize, long style=wxDEFAULT_DIALOG_STYLE, const wxString &name=wxDialogNameStr);
                
                enzyme GetEnzyme() {return e;}
                
                void OnTextID(wxCommandEvent& event);
                void OnTextPattern(wxCommandEvent& event);
                void OnTextFN(wxCommandEvent& event);
                void OnTextFP(wxCommandEvent& event);
                void OnTextLabel(wxCommandEvent& event);
};

enum {
        wxID_EnzymeID = wxID_HIGHEST + 1,
        wxID_EnzymePattern = wxID_HIGHEST + 2,
        wxID_EnzymeFN = wxID_HIGHEST + 3,
        wxID_EnzymeFP = wxID_HIGHEST + 4,
        wxID_EnzymeLabel = wxID_HIGHEST + 5
};

#endif
