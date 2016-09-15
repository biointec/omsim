#ifndef MAINFRAME_HPP
#define MAINFRAME_HPP

#include "wx.hpp"
#include <wx/dialog.h>
#include <wx/notebook.h>

#include <map>

#include "configuration.hpp"

class BasicPanel;
class AdvancedPanel;
class MainFrame : public wxFrame
{
        private:
                configuration c;
                std::map<wxString, enzyme> enzymes;
                BasicPanel *bpanel;
                AdvancedPanel *apanel;
        public:
                MainFrame(const wxString& title);
                void update();
                void OnNew(wxCommandEvent& event);
                void OnOpen(wxCommandEvent& event);
                void OnSave(wxCommandEvent& event);
                void OnCopy(wxCommandEvent& event);
                void OnQuit(wxCommandEvent& event);
};

enum {
        wxID_CNEW = wxID_HIGHEST + 1,
        wxID_COPEN = wxID_HIGHEST + 2,
        wxID_CSAVE = wxID_HIGHEST + 3,
        wxID_CCOPY = wxID_HIGHEST + 4
};
#endif
