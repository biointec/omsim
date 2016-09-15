#ifndef BASICPANEL_HPP
#define BASICPANEL_HPP

#include <map>
#include "wx.hpp"
#include "configuration.hpp"

class TagPanel;

class BasicPanel : public wxPanel
{
        private:
                configuration &c;
                std::map<wxString, enzyme> &enzymes;
                wxTextCtrl *nameCtrl;
                wxListBox *fastaListBox;
                wxListBox *xmlListBox;
                wxCheckListBox *enzymeCheckListBox;
                wxTextCtrl *sizeMeanCtrl;
                wxTextCtrl *sizeSDCtrl;
                wxCheckBox *circularCheckBox;
                std::vector<TagPanel*> tags;
        public:
                BasicPanel(wxWindow *parent, wxWindowID id, configuration &c_, std::map<wxString, enzyme> &enzymes_);
                void update();
                void OnEnzDblClick(wxCommandEvent& event);
                void OnName(wxCommandEvent& Event);
                void OnSizeMean(wxCommandEvent& Event);
                void OnSizeSD(wxCommandEvent& Event);
                void OnCircularCheck(wxCommandEvent& Event);
                
                void addFasta(wxString fasta);
                void removeFasta(wxString fasta);
                void clearFasta();
};

enum {
        wxID_FastaListBox = wxID_HIGHEST + 1,
        wxID_EnzymeCheckListBox = wxID_HIGHEST + 2,
        wxID_SizeMean = wxID_HIGHEST + 3,
        wxID_SizeSD = wxID_HIGHEST + 4,
        wxID_CircularCheckBox = wxID_HIGHEST + 5,
        wxID_Name = wxID_HIGHEST + 6
};

#endif
