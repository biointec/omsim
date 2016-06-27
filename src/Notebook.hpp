#ifndef NOTEBOOK_HPP
#define NOTEBOOK_HPP

#include "wx.hpp"
#include <wx/dialog.h>
#include <wx/notebook.h>

#include <map>

#include "configuration.hpp"

class Notebook : public wxDialog
{
        private:
                configuration c;
                std::map<wxString, enzyme> enzymes;
        public:
                Notebook(wxWindow *parent, wxWindowID id, const wxString &title, const configuration &c_=configuration(), const std::map<wxString, enzyme> &enzymes_=std::map<wxString, enzyme>(), const wxPoint &pos=wxDefaultPosition, const wxSize &size=wxDefaultSize, long style=wxDEFAULT_DIALOG_STYLE, const wxString &name=wxDialogNameStr);
                configuration GetConfiguration() {return c;}
};

#endif
