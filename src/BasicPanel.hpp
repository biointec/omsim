#ifndef BASICPANEL_HPP
#define BASICPANEL_HPP

#include "wx.hpp"

class EnzymePanel;
class ConfigurationPanel;

class BasicPanel : public wxPanel
{
        private:
                wxListBox *fastaListBox;
                wxListBox *xmlListBox;
                wxCheckListBox *configurationCheckListBox;
                ConfigurationPanel *configurationPanel;
                wxCheckListBox *enzymeCheckListBox;
                EnzymePanel *enzymePanel;
        public:
                BasicPanel(wxWindow *parent, wxWindowID id);
                void OnEnzDblClick(wxCommandEvent& event);
                void OnConfDblClick(wxCommandEvent& event);
};

enum {
        ID_XMLListBox = wxID_HIGHEST + 1,
        ID_FastaListBox = wxID_HIGHEST + 2,
        ID_ConfigurationCheckListBox = wxID_HIGHEST + 3,
        ID_EnzymeCheckListBox = wxID_HIGHEST + 4
};

#endif
