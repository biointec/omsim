#ifndef MAINFRAME_HPP
#define MAINFRAME_HPP

#include "wx.hpp"
#include "ConfigurationPanel.hpp"
#include "EnzymePanel.hpp"

#include <thread>

class EnzymePanel;
class ConfigurationPanel;

class MainFrame : public wxFrame
{
        private:
                wxCheckListBox *configurationCheckListBox;
                ConfigurationPanel *configurationPanel;
                wxListBox *enzymeListBox;
                EnzymePanel *enzymePanel;
                std::map<wxString, configuration> configurations;
                std::map<wxString, enzyme> enzymes;
                
                std::thread simulator_thread;
        public:
                MainFrame(const wxString& title);
                
                void OnQuit(wxCommandEvent& event);
                void OnEnzDblClick(wxCommandEvent& event);
                void OnConfDblClick(wxCommandEvent& event);
                void OnRunOmsim(wxCommandEvent& event);
                
                void update();
};

enum {
        wxID_ConfigurationCheckListBox = wxID_HIGHEST + 1,
        wxID_EnzymeCheckListBox = wxID_HIGHEST + 2,
        wxID_RunButton = wxID_HIGHEST + 3
};

#endif
