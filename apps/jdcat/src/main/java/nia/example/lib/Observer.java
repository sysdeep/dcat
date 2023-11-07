package nia.example.lib;

public interface Observer {
    // method to update the observer, used by subject
    public void update(String event);

    // // attach with subject to observe
    // public void setSubject(Subject sub);
}
