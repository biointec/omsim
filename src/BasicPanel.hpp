#ifndef BASICPANEL_HPP
#define BASICPANEL_HPP

#include "wx.hpp"
#include <wx/stattext.h>

class BasicPanel : public wxPanel
{
        private:
                wxListBox *fastaListBox;
                wxListBox *xmlListBox;
                wxCheckListBox *enzymeCheckListBox;
        public:
                BasicPanel(wxWindow *parent, wxWindowID id);
};

enum {
        ID_XMLListBox = wxID_HIGHEST + 1,
        ID_FastaListBox = wxID_HIGHEST + 2,
        ID_EnzymeCheckListBox = wxID_HIGHEST + 3
};

#endif
