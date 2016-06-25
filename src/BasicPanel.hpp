#ifndef BASICPANEL_HPP
#define BASICPANEL_HPP

#include "wx.hpp"
#include <wx/stattext.h>
#include "ListBoxPanel.hpp"

class BasicPanel : public wxPanel
{
        private:
                wxListBox * fastaListBox;
                wxListBox * xmlListBox;
        public:
                BasicPanel(wxWindow *parent, wxWindowID id);
};

enum {
        ID_XMLListBox = wxID_HIGHEST + 1,
        ID_FastaListBox = wxID_HIGHEST + 2
};

#endif
