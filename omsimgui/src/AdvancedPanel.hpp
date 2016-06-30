#ifndef ADVANCEDPANEL_HPP
#define ADVANCEDPANEL_HPP

#include "wx.hpp"

#include "configuration.hpp"

class AdvancedPanel : public wxPanel
{
        private:
                configuration &c;
        public:
                AdvancedPanel(wxWindow *parent, wxWindowID id, configuration &c_);
};

#endif
