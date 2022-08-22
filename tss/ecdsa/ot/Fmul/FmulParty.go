package Fmul

import (
	"github.com/cloudflare/circl/group"
	"github.com/cloudflare/circl/ot/simplestOT"
)

type SenderFmul struct {
	a             group.Scalar             // The input of the sender
	deltas        []group.Scalar           // The n random of the sender
	m0s           [][]byte                 // The n m0 messages of the sender
	m1s           [][]byte                 // The n m1 messages of the sender
	baseOTsenders []simplestOT.SenderSimOT // The n senders for n baseOT
	s1            group.Scalar             // The final additive share
	myGroup       group.Group              // The elliptic curve we operate in
}

type ReceiverFmul struct {
	b               group.Scalar               // The input of the receiver
	ts              []int                      // The n choice bits of the receiver, either 0 or 1
	tsScalar        []group.Scalar             // The scalar version of n choice bits, either -1 or 1
	zs              []group.Scalar             // The n OT transfered messages from the sender
	vs              []group.Scalar             // The n random of the receiver such that v*t = b
	sigma           group.Scalar               // The blinding scalar
	baseOTreceivers []simplestOT.ReceiverSimOT // The n receivers for n baseOT
	s2              group.Scalar               // The final additive share
	myGroup         group.Group                // The elliptic curve we operate in
}