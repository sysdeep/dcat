package nia.ui.explorer.files;

import java.awt.event.KeyEvent;
import java.awt.event.KeyListener;
import java.awt.event.MouseEvent;
import java.awt.event.MouseListener;

import javax.swing.JList;

public class ListActionsHandler implements KeyListener, MouseListener {
    JList<String> _list;
    IActions _actions_consumer;

    public ListActionsHandler(JList<String> list, IActions actions_consumer) {
        _list = list;
        _actions_consumer = actions_consumer;
        _list.addKeyListener(this);
        _list.addMouseListener(this);
    }

    // KeyListener ------------------------------------------------------------
    @Override
    public void keyPressed(KeyEvent e) {
        if (e.getKeyCode() == KeyEvent.VK_ENTER) {
            _actions_consumer.do_open();
        }
    }

    @Override
    public void keyReleased(KeyEvent arg0) {
    }

    @Override
    public void keyTyped(KeyEvent arg0) {
    }

    // MouseListener ----------------------------------------------------------
    @Override
    public void mouseClicked(MouseEvent e) {
        if (e.getClickCount() == 2 && !e.isConsumed()) {
            e.consume();
            // System.out.println("Double Click");
            _actions_consumer.do_open();
        }
    }

    @Override
    public void mouseEntered(MouseEvent arg0) {
    }

    @Override
    public void mouseExited(MouseEvent arg0) {
    }

    @Override
    public void mousePressed(MouseEvent arg0) {
    }

    @Override
    public void mouseReleased(MouseEvent arg0) {
    }

}
