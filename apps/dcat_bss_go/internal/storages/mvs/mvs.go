package mvs

// TODO
// MVS - multi volume sqlite storage
type MVS struct {
}

func NewMVS() *MVS {
	return &MVS{}
}

func (m *MVS) Open(filePath string) error {
	// TODO
	return nil
}

func (m *MVS) GetVolumes() {}
