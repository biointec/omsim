#ifndef TAGPANEL_HPP
#define TAGPANEL_HPP

#include "wx.hpp"

class TagPanel : public wxPanel
{
        private:
                wxStaticText *label;
                wxTextCtrl *ctrl;
                
                wxString const &tag;
                wxString &val;
                wxString const &lab;
        public:
                TagPanel(wxWindow *parent, wxSizer *grid, wxString const &tag_, wxString &val_, wxString const &lab_);
                
                void OnText(wxCommandEvent& event);
};

enum {
        wxID_Ctrl = wxID_HIGHEST + 1
};

#endif
