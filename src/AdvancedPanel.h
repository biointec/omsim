#ifndef ADVANCEDPANEL_HPP
#define ADVANCEDPANEL_HPP

#include "wx.hpp"

class AdvancedPanel : public wxPanel
{
        public:
                AdvancedPanel(wxWindow *parent, wxWindowID id)
                      : wxPanel(parent, id)
                {
                        wxBoxSizer *vbox = new wxBoxSizer(wxVERTICAL);
                        
                        wxBoxSizer *hbox1 = new wxBoxSizer(wxVERTICAL);
                        wxButton *ok = new wxButton(this, -1, wxT("Ok"));
                        hbox1->Add(ok);
                        vbox->Add(hbox1);
                        
                        wxBoxSizer *hbox2 = new wxBoxSizer(wxVERTICAL);
                        wxButton *cancel = new wxButton(this, -1, wxT("Cancel"));
                        hbox2->Add(cancel);
                        vbox->Add(hbox2);
                        
                        SetSizer(vbox);
                }
};

#endif
