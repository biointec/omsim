#ifndef LISTBOXPANEL_HPP
#define LISTBOXPANEL_HPP

#include <wx/wx.h>
#include <wx/listbox.h>

class ListBoxPanel : public wxPanel
{
        private:
                wxString Ext;
                wxString ext;
        public:
                ListBoxPanel(wxPanel *parent, wxListBox * lb, wxString const &Ext_, wxString const &ext_);
                void OnNew(wxCommandEvent& event);
                void OnClear(wxCommandEvent& event);
                void OnDelete(wxCommandEvent& event);
                
                wxListBox *m_lb;

                wxButton *m_newb;
                wxButton *m_clearb;
                wxButton *m_deleteb;
};

#endif
