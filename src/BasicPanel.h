#ifndef BASICPANEL_HPP
#define BASICPANEL_HPP

#include "wx.hpp"

class BasicPanel : public wxPanel
{
        public:
                BasicPanel(wxWindow *parent, wxWindowID id)
                      : wxPanel(parent, id)
                {
                        wxBoxSizer *vbox = new wxBoxSizer(wxVERTICAL);
                        wxBoxSizer *hbox1 = new wxBoxSizer(wxHORIZONTAL);
                        wxBoxSizer *hbox2 = new wxBoxSizer(wxHORIZONTAL);
                        
                        wxButton *ok = new wxButton(this, -1, wxT("Ok"));
                        hbox1->Add(ok);
                        
                        wxButton *cancel = new wxButton(this, -1, wxT("Cancel"));
                        hbox2->Add(cancel);
                        
                        vbox->Add(hbox1);
                        vbox->Add(hbox2);
                        
                        SetSizer(vbox);
                }
};

#endif
