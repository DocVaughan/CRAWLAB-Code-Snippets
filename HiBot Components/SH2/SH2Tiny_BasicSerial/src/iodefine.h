/************************************************************************/
/*      SH7047 Series Include File                          Ver 2.5     */
/************************************************************************/
struct st_sci {                                         /* struct SCI   */
              union {                                   /* SMR          */
                    unsigned char BYTE;                 /*  Byte Access */
                    struct {                            /*  Bit  Access */
                           unsigned char CA  :1;        /*    C/A       */
                           unsigned char CHR :1;        /*    CHR       */
                           unsigned char _PE :1;        /*    PE        */
                           unsigned char OE  :1;        /*    O/E       */
                           unsigned char STOP:1;        /*    STOP      */
                           unsigned char MP  :1;        /*    MP        */
                           unsigned char CKS :2;        /*    CKS       */
                           }      BIT;                  /*              */
                    }           SMR;                    /*              */
              unsigned char     BRR;                    /* BRR          */
              union {                                   /* SCR          */
                    unsigned char BYTE;                 /*  Byte Access */
                    struct {                            /*  Bit  Access */
                           unsigned char TIE :1;        /*    TIE       */
                           unsigned char RIE :1;        /*    RIE       */
                           unsigned char TE  :1;        /*    TE        */
                           unsigned char RE  :1;        /*    RE        */
                           unsigned char MPIE:1;        /*    MPIE      */
                           unsigned char TEIE:1;        /*    TEIE      */
                           unsigned char CKE :2;        /*    CKE       */
                           }      BIT;                  /*              */
                    }           SCR;                    /*              */
              unsigned char     TDR;                    /* TDR          */
              union {                                   /* SSR          */
                    unsigned char BYTE;                 /*  Byte Access */
                    struct {                            /*  Bit  Access */
                           unsigned char TDRE:1;        /*    TDRE      */
                           unsigned char RDRF:1;        /*    RDRF      */
                           unsigned char ORER:1;        /*    ORER      */
                           unsigned char FER :1;        /*    FER       */
                           unsigned char PER :1;        /*    PER       */
                           unsigned char TEND:1;        /*    TEND      */
                           unsigned char MPB :1;        /*    MPB       */
                           unsigned char MPBT:1;        /*    MPBT      */
                           }      BIT;                  /*              */
                    }           SSR;                    /*              */
              unsigned char     RDR;                    /* RDR          */
              union {                                   /* SDCR         */
                    unsigned char BYTE;                 /*  Byte Access */
                    struct {                            /*  Bit  Access */
                           unsigned char    :4;         /*              */
                           unsigned char DIR:1;         /*    DIR       */
                           }      BIT;                  /*              */
                    }           SDCR;                   /*              */
};                                                      /*              */
struct st_mtu {                                         /* struct MTU   */
              union {                                   /* TOER         */
                    unsigned char BYTE;                 /*  Byte Access */
                    struct {                            /*  Bit  Access */
                           unsigned char     :2;        /*              */
                           unsigned char OE4D:1;        /*    OE4D      */
                           unsigned char OE4C:1;        /*    OE4C      */
                           unsigned char OE3D:1;        /*    OE3D      */
                           unsigned char OE4B:1;        /*    OE4B      */
                           unsigned char OE4A:1;        /*    OE4A      */
                           unsigned char OE3B:1;        /*    OE3B      */
                           }      BIT;                  /*              */
                    }           TOER;                   /*              */
              union {                                   /* TOCR         */
                    unsigned char BYTE;                 /*  Byte Access */
                    struct {                            /*  Bit  Access */
                           unsigned char     :1;        /*              */
                           unsigned char PSYE:1;        /*    PSYE      */
                           unsigned char     :4;        /*              */
                           unsigned char OLSN:1;        /*    OLSN      */
                           unsigned char OLSP:1;        /*    OLSP      */
                           }      BIT;                  /*              */
                    }           TOCR;                   /*              */
              char              wk1;                    /*              */
              union {                                   /* TGCR         */
                    unsigned char BYTE;                 /*  Byte Access */
                    struct {                            /*  Bit  Access */
                           unsigned char    :1;         /*              */
                           unsigned char BDC:1;         /*    BDC       */
                           unsigned char N  :1;         /*    N         */
                           unsigned char P  :1;         /*    P         */
                           unsigned char FB :1;         /*    FB        */
                           unsigned char WF :1;         /*    WF        */
                           unsigned char VF :1;         /*    VF        */
                           unsigned char UF :1;         /*    UF        */
                           }      BIT;                  /*              */
                    }           TGCR;                   /*              */
              char              wk2[6];                 /*              */
              unsigned short    TCDR;                   /* TCDR         */
              unsigned short    TDDR;                   /* TDDR         */
              char              wk3[8];                 /*              */
              unsigned short    TCNTS;                  /* TCNTS        */
              unsigned short    TCBR;                   /* TCBR         */
              char              wk4[28];                /*              */
              union {                                   /* TSTR         */
                    unsigned char BYTE;                 /*  Byte Access */
                    struct {                            /*  Bit  Access */
                           unsigned char CST4:1;        /*    CST4      */
                           unsigned char CST3:1;        /*    CST3      */
                           unsigned char     :3;        /*              */
                           unsigned char CST2:1;        /*    CST2      */
                           unsigned char CST1:1;        /*    CST1      */
                           unsigned char CST0:1;        /*    CST0      */
                           }      BIT;                  /*              */
                    }           TSTR;                   /*              */
              union {                                   /* TSYR         */
                    unsigned char BYTE;                 /*  Byte Access */
                    struct {                            /*  Bit  Access */
                           unsigned char SYNC4:1;       /*    SYNC4     */
                           unsigned char SYNC3:1;       /*    SYNC3     */
                           unsigned char      :3;       /*              */
                           unsigned char SYNC2:1;       /*    SYNC2     */
                           unsigned char SYNC1:1;       /*    SYNC1     */
                           unsigned char SYNC0:1;       /*    SYNC0     */
                           }      BIT;                  /*              */
                    }           TSYR;                   /*              */
};                                                      /*              */
struct st_mtu0 {                                        /* struct MTU0  */
               union {                                  /* TCR          */
                     unsigned char BYTE;                /*  Byte Access */
                     struct {                           /*  Bit  Access */
                            unsigned char CCLR:3;       /*    CCLR      */
                            unsigned char CKEG:2;       /*    CKEG      */
                            unsigned char TPSC:3;       /*    TPSC      */
                            }      BIT;                 /*              */
                     }          TCR;                    /*              */
               union {                                  /* TMDR         */
                     unsigned char BYTE;                /*  Byte Access */
                     struct {                           /*  Bit  Access */
                            unsigned char    :2;        /*              */
                            unsigned char BFB:1;        /*    BFB       */
                            unsigned char BFA:1;        /*    BFA       */
                            unsigned char MD :4;        /*    MD        */
                            }      BIT;                 /*              */
                     }          TMDR;                   /*              */
               union {                                  /* TIOR         */
                     unsigned short WORD;               /*  Word Access */
                     struct {                           /*  Byte Access */
                            unsigned char H;            /*    TIORH     */
                            unsigned char L;            /*    TIORL     */
                            }       BYTE;               /*              */
                     struct {                           /*  Bit  Access */
                            unsigned char IOB:4;        /*    IOB       */
                            unsigned char IOA:4;        /*    IOA       */
                            unsigned char IOD:4;        /*    IOD       */
                            unsigned char IOC:4;        /*    IOC       */
                            }       BIT;                /*              */
                     }          TIOR;                   /*              */
               union {                                  /* TIER         */
                     unsigned char BYTE;                /*  Byte Access */
                     struct {                           /*  Bit  Access */
                            unsigned char TTGE :1;      /*    TTGE      */
                            unsigned char      :2;      /*              */
                            unsigned char TCIEV:1;      /*    TCIEV     */
                            unsigned char TGIED:1;      /*    TGIED     */
                            unsigned char TGIEC:1;      /*    TGIEC     */
                            unsigned char TGIEB:1;      /*    TGIEB     */
                            unsigned char TGIEA:1;      /*    TGIEA     */
                            }      BIT;                 /*              */
                     }          TIER;                   /*              */
               union {                                  /* TSR          */
                     unsigned char BYTE;                /*  Byte Access */
                     struct {                           /*  Bit  Access */
                            unsigned char     :3;       /*              */
                            unsigned char TCFV:1;       /*    TCFV      */
                            unsigned char TGFD:1;       /*    TGFD      */
                            unsigned char TGFC:1;       /*    TGFC      */
                            unsigned char TGFB:1;       /*    TGFB      */
                            unsigned char TGFA:1;       /*    TGFA      */
                            }      BIT;                 /*              */
                     }          TSR;                    /*              */
               unsigned short   TCNT;                   /* TCNT         */
               unsigned short   TGRA;                   /* TGRA         */
               unsigned short   TGRB;                   /* TGRB         */
               unsigned short   TGRC;                   /* TGRC         */
               unsigned short   TGRD;                   /* TGRD         */
};                                                      /*              */
struct st_mtu1 {                                        /* struct MTU1  */
               union {                                  /* TCR          */
                     unsigned char BYTE;                /*  Byte Access */
                     struct {                           /*  Bit  Access */
                            unsigned char     :1;       /*              */
                            unsigned char CCLR:2;       /*    CCLR      */
                            unsigned char CKEG:2;       /*    CKEG      */
                            unsigned char TPSC:3;       /*    TPSC      */
                            }      BIT;                 /*              */
                     }          TCR;                    /*              */
               union {                                  /* TMDR         */
                     unsigned char BYTE;                /*  Byte Access */
                     struct {                           /*  Bit  Access */
                            unsigned char   :4;         /*              */
                            unsigned char MD:4;         /*    MD        */
                            }      BIT;                 /*              */
                     }          TMDR;                   /*              */
               union {                                  /* TIOR         */
                     unsigned char BYTE;                /*  Byte Access */
                     struct {                           /*  Bit  Access */
                            unsigned char IOB:4;        /*    IOB       */
                            unsigned char IOA:4;        /*    IOA       */
                            }      BIT;                 /*              */
                     }          TIOR;                   /*              */
               char             wk;                     /*              */
               union {                                  /* TIER         */
                     unsigned char BYTE;                /*  Byte Access */
                     struct {                           /*  Bit  Access */
                            unsigned char TTGE :1;      /*    TTGE      */
                            unsigned char      :1;      /*              */
                            unsigned char TCIEU:1;      /*    TCIEU     */
                            unsigned char TCIEV:1;      /*    TCIEV     */
                            unsigned char      :2;      /*              */
                            unsigned char TGIEB:1;      /*    TGIEB     */
                            unsigned char TGIEA:1;      /*    TGIEA     */
                            }      BIT;                 /*              */
                     }          TIER;                   /*              */
               union {                                  /* TSR          */
                     unsigned char BYTE;                /*  Byte Access */
                     struct {                           /*  Bit  Access */
                            unsigned char TCFD:1;       /*    TCFD      */
                            unsigned char     :1;       /*              */
                            unsigned char TCFU:1;       /*    TCFU      */
                            unsigned char TCFV:1;       /*    TCFV      */
                            unsigned char     :2;       /*              */
                            unsigned char TGFB:1;       /*    TGFB      */
                            unsigned char TGFA:1;       /*    TGFA      */
                            }      BIT;                 /*              */
                     }          TSR;                    /*              */
               unsigned short   TCNT;                   /* TCNT         */
               unsigned short   TGRA;                   /* TGRA         */
               unsigned short   TGRB;                   /* TGRB         */
};                                                      /*              */
struct st_mtu3 {                                        /* struct MTU3  */
               union {                                  /* TCR          */
                     unsigned char BYTE;                /*  Byte Access */
                     struct {                           /*  Bit  Access */
                            unsigned char CCLR:3;       /*    CCLR      */
                            unsigned char CKEG:2;       /*    CKEG      */
                            unsigned char TPSC:3;       /*    TPSC      */
                            }      BIT;                 /*              */
                     }          TCR;                    /*              */
               char             wk1;                    /*              */
               union {                                  /* TMDR         */
                     unsigned char BYTE;                /*  Byte Access */
                     struct {                           /*  Bit  Access */
                            unsigned char    :2;        /*              */
                            unsigned char BFB:1;        /*    BFB       */
                            unsigned char BFA:1;        /*    BFA       */
                            unsigned char MD :4;        /*    MD        */
                            }      BIT;                 /*              */
                     }          TMDR;                   /*              */
               char             wk2;                    /*              */
               union {                                  /* TIOR         */
                     unsigned short WORD;               /*  Word Access */
                     struct {                           /*  Byte Access */
                            unsigned char H;            /*    TIORH     */
                            unsigned char L;            /*    TIORL     */
                            }       BYTE;               /*              */
                     struct {                           /*  Bit  Access */
                            unsigned char IOB:4;        /*    IOB       */
                            unsigned char IOA:4;        /*    IOA       */
                            unsigned char IOD:4;        /*    IOD       */
                            unsigned char IOC:4;        /*    IOC       */
                            }       BIT;                /*              */
                     }          TIOR;                   /*              */
               char             wk3[2];                 /*              */
               union {                                  /* TIER         */
                     unsigned char BYTE;                /*  Byte Access */
                     struct {                           /*  Bit  Access */
                            unsigned char TTGE :1;      /*    TTGE      */
                            unsigned char      :2;      /*              */
                            unsigned char TCIEV:1;      /*    TCIEV     */
                            unsigned char TGIED:1;      /*    TGIED     */
                            unsigned char TGIEC:1;      /*    TGIEC     */
                            unsigned char TGIEB:1;      /*    TGIEB     */
                            unsigned char TGIEA:1;      /*    TGIEA     */
                            }      BIT;                 /*              */
                     }          TIER;                   /*              */
               char             wk4[7];                 /*              */
               unsigned short   TCNT;                   /* TCNT         */
               char             wk5[6];                 /*              */
               unsigned short   TGRA;                   /* TGRA         */
               unsigned short   TGRB;                   /* TGRB         */
               char             wk6[8];                 /*              */
               unsigned short   TGRC;                   /* TGRC         */
               unsigned short   TGRD;                   /* TGRD         */
               char             wk7[4];                 /*              */
               union {                                  /* TSR          */
                     unsigned char BYTE;                /*  Byte Access */
                     struct {                           /*  Bit  Access */
                            unsigned char TCFD:1;       /*    TCFD      */
                            unsigned char     :2;       /*              */
                            unsigned char TCFV:1;       /*    TCFV      */
                            unsigned char TGFD:1;       /*    TGFD      */
                            unsigned char TGFC:1;       /*    TGFC      */
                            unsigned char TGFB:1;       /*    TGFB      */
                            unsigned char TGFA:1;       /*    TGFA      */
                            }      BIT;                 /*              */
                     }          TSR;                    /*              */
};                                                      /*              */
struct st_mtu4 {                                        /* struct MTU4  */
               char             wk1;                    /*              */
               union {                                  /* TCR          */
                     unsigned char BYTE;                /*  Byte Access */
                     struct {                           /*  Bit  Access */
                            unsigned char CCLR:3;       /*    CCLR      */
                            unsigned char CKEG:2;       /*    CKEG      */
                            unsigned char TPSC:3;       /*    TPSC      */
                            }      BIT;                 /*              */
                     }          TCR;                    /*              */
               char             wk2;                    /*              */
               union {                                  /* TMDR         */
                     unsigned char BYTE;                /*  Byte Access */
                     struct {                           /*  Bit  Access */
                            unsigned char    :2;        /*              */
                            unsigned char BFB:1;        /*    BFB       */
                            unsigned char BFA:1;        /*    BFA       */
                            unsigned char MD :4;        /*    MD        */
                            }      BIT;                 /*              */
                     }          TMDR;                   /*              */
               char             wk3[2];                 /*              */
               union {                                  /* TIOR         */
                     unsigned short WORD;               /*  Word Access */
                     struct {                           /*  Byte Access */
                            unsigned char H;            /*    TIORH     */
                            unsigned char L;            /*    TIORL     */
                            }       BYTE;               /*              */
                     struct {                           /*  Bit  Access */
                            unsigned char IOB:4;        /*    IOB       */
                            unsigned char IOA:4;        /*    IOA       */
                            unsigned char IOD:4;        /*    IOD       */
                            unsigned char IOC:4;        /*    IOC       */
                            }       BIT;                /*              */
                     }          TIOR;                   /*              */
               char             wk4;                    /*              */
               union {                                  /* TIER         */
                     unsigned char BYTE;                /*  Byte Access */
                     struct {                           /*  Bit  Access */
                            unsigned char TTGE :1;      /*    TTGE      */
                            unsigned char      :2;      /*              */
                            unsigned char TCIEV:1;      /*    TCIEV     */
                            unsigned char TGIED:1;      /*    TGIED     */
                            unsigned char TGIEC:1;      /*    TGIEC     */
                            unsigned char TGIEB:1;      /*    TGIEB     */
                            unsigned char TGIEA:1;      /*    TGIEA     */
                            }      BIT;                 /*              */
                     }          TIER;                   /*              */
               char             wk5[8];                 /*              */
               unsigned short   TCNT;                   /* TCNT         */
               char             wk6[8];                 /*              */
               unsigned short   TGRA;                   /* TGRA         */
               unsigned short   TGRB;                   /* TGRB         */
               char             wk7[8];                 /*              */
               unsigned short   TGRC;                   /* TGRC         */
               unsigned short   TGRD;                   /* TGRD         */
               char             wk8;                    /*              */
               union {                                  /* TSR          */
                     unsigned char BYTE;                /*  Byte Access */
                     struct {                           /*  Bit  Access */
                            unsigned char TCFD:1;       /*    TCFD      */
                            unsigned char     :2;       /*              */
                            unsigned char TCFV:1;       /*    TCFV      */
                            unsigned char TGFD:1;       /*    TGFD      */
                            unsigned char TGFC:1;       /*    TGFC      */
                            unsigned char TGFB:1;       /*    TGFB      */
                            unsigned char TGFA:1;       /*    TGFA      */
                            }      BIT;                 /*              */
                     }          TSR;                    /*              */
};                                                      /*              */
struct st_poe {                                         /* struct POE   */
              union {                                   /* ICSR1        */
                    unsigned short WORD;                /*  Word Access */
                    struct {                            /*  Bit  Access */
                           unsigned char POE3F:1;       /*    POE3F     */
                           unsigned char POE2F:1;       /*    POE2F     */
                           unsigned char POE1F:1;       /*    POE1F     */
                           unsigned char POE0F:1;       /*    POE0F     */
                           unsigned char      :3;       /*              */
                           unsigned char PIE  :1;       /*    PIE       */
                           unsigned char POE3M:2;       /*    POE3M     */
                           unsigned char POE2M:2;       /*    POE2M     */
                           unsigned char POE1M:2;       /*    POE1M     */
                           unsigned char POE0M:2;       /*    POE0M     */
                           }       BIT;                 /*              */
              }                 ICSR1;                  /*              */
              union {                                   /* OCSR         */
                    unsigned char BYTE;                 /*  Byte Access */
                    struct {                            /*  Bit  Access */
                           unsigned char OSF:1;         /*    OSF       */
                           unsigned char    :5;         /*              */
                           unsigned char OCE:1;         /*    OCE       */
                           unsigned char OIE:1;         /*    OIE       */
                           }      BIT;                  /*              */
                    }           OCSR;                   /*              */
              union {                                   /* ICSR2        */
                    unsigned short WORD;                /*  Word Access */
                    struct {                            /*  Bit  Access */
                           unsigned char      :1;       /*              */
                           unsigned char POE6F:1;       /*    POE6F     */
                           unsigned char POE5F:1;       /*    POE5F     */
                           unsigned char POE4F:1;       /*    POE4F     */
                           unsigned char      :3;       /*              */
                           unsigned char PIE  :1;       /*    PIE       */
                           unsigned char      :2;       /*              */
                           unsigned char POE6M:2;       /*    POE6M     */
                           unsigned char POE5M:2;       /*    POE5M     */
                           unsigned char POE4M:2;       /*    POE4M     */
                           }       BIT;                 /*              */
              }                 ICSR2;                  /*              */
};                                                      /*              */
struct st_intc {                                        /* struct INTC  */
               union {                                  /* IPRA         */
                     unsigned short WORD;               /*  Word Access */
                     struct {                           /*  Bit  Access */
                            unsigned char _IRQ0:4;      /*    IRQ0      */
                            unsigned char _IRQ1:4;      /*    IRQ1      */
                            unsigned char _IRQ2:4;      /*    IRQ2      */
                            unsigned char _IRQ3:4;      /*    IRQ3      */
                            }       BIT;                /*              */
                     }          IPRA;                   /*              */
               char             wk1[4];                 /*              */
               union {                                  /* IPRD         */
                     unsigned short WORD;               /*  Word Access */
                     struct {                           /*  Bit  Access */
                            unsigned char _MTU0G:4;     /*    MTU0 TGI  */
                            unsigned char _MTU0C:4;     /*    MTU0 TCI  */
                            unsigned char _MTU1G:4;     /*    MTU1 TGI  */
                            unsigned char _MTU1C:4;     /*    MTU1 TCI  */
                            }       BIT;                /*              */
                     }          IPRD;                   /*              */
               union {                                  /* IPRE         */
                     unsigned short WORD;               /*  Word Access */
                     struct {                           /*  Bit  Access */
                            unsigned char _MTU2G:4;     /*    MTU2 TGI  */
                            unsigned char _MTU2C:4;     /*    MTU2 TCI  */
                            unsigned char _MTU3G:4;     /*    MTU3 TGI  */
                            unsigned char _MTU3C:4;     /*    MTU3 TCI  */
                            }       BIT;                /*              */
                     }          IPRE;                   /*              */
               union {                                  /* IPRF         */
                     unsigned short WORD;               /*  Word Access */
                     struct {                           /*  Bit  Access */
                            unsigned char _MTU4G:4;     /*    MTU4 TGI  */
                            unsigned char _MTU4C:4;     /*    MTU4 TCI  */
                            }       BIT;                /*              */
                     }          IPRF;                   /*              */
               union {                                  /* IPRG         */
                     unsigned short WORD;               /*  Word Access */
                     struct {                           /*  Bit  Access */
                            unsigned char _AD01:4;      /*    A/D0,1    */
                            unsigned char _DTC :4;      /*    DTC       */
                            unsigned char _CMT0:4;      /*    CMT0      */
                            unsigned char _CMT1:4;      /*    CMT1      */
                            }       BIT;                /*              */
                     }          IPRG;                   /*              */
               union {                                  /* IPRH         */
                     unsigned short WORD;               /*  Word Access */
                     struct {                           /*  Bit  Access */
                            unsigned char _WDT:4;       /*    WDT       */
                            unsigned char _IO :4;       /*    I/O(MTU)  */
                            }       BIT;                /*              */
                     }          IPRH;                   /*              */
               union {                                  /* ICR1         */
                     unsigned short WORD;               /*  Word Access */
                     struct {                           /*  Bit  Access */
                            unsigned char NMIL :1;      /*    NMIL      */
                            unsigned char      :6;      /*              */
                            unsigned char NMIE :1;      /*    NMIE      */
                            unsigned char IRQ0S:1;      /*    IRQ0S     */
                            unsigned char IRQ1S:1;      /*    IRQ1S     */
                            unsigned char IRQ2S:1;      /*    IRQ2S     */
                            unsigned char IRQ3S:1;      /*    IRQ3S     */
                            }       BIT;                /*              */
                     }          ICR1;                   /*              */
               union {                                  /* ISR          */
                     unsigned short WORD;               /*  Word Access */
                     struct {                           /*  Bit  Access */
                            unsigned char      :8;      /*              */
                            unsigned char IRQ0F:1;      /*    IRQ0F     */
                            unsigned char IRQ1F:1;      /*    IRQ1F     */
                            unsigned char IRQ2F:1;      /*    IRQ2F     */
                            unsigned char IRQ3F:1;      /*    IRQ3F     */
                            }       BIT;                /*              */
                     }          ISR;                    /*              */
               union {                                  /* IPRI         */
                     unsigned short WORD;               /*  Word Access */
                     struct {                           /*  Bit  Access */
                            unsigned char _SCI2:4;      /*    SCI2      */
                            unsigned char _SCI3:4;      /*    SCI3      */
                            unsigned char _SCI4:4;      /*    SCI4      */
                            unsigned char _MMT :4;      /*    MMT       */
                            }       BIT;                /*              */
                     }          IPRI;                   /*              */
               char             wk2[2];                 /*              */
               union {                                  /* IPRK         */
                     unsigned short WORD;               /*  Word Access */
                     struct {                           /*  Bit  Access */
                            unsigned char _IO   :4;     /*    I/O(MMT)  */
                            unsigned char       :4;     /*              */
                            unsigned char _HCAN2:4;     /*    HCAN2     */
                            }       BIT;                /*              */
                     }          IPRK;                   /*              */
               char             wk3[4];                 /*              */
               union {                                  /* ICR2         */
                     unsigned short WORD;               /*  Word Access */
                     struct {                           /*  Bit  Access */
                            unsigned char IRQ0ES:2;     /*    IRQ0ES    */
                            unsigned char IRQ1ES:2;     /*    IRQ1ES    */
                            unsigned char IRQ2ES:2;     /*    IRQ2ES    */
                            unsigned char IRQ3ES:2;     /*    IRQ3ES    */
                            }       BIT;                /*              */
                     }          ICR2;                   /*              */
};                                                      /*              */
struct st_pa {                                          /* struct PA    */
             union {                                    /* PADRL        */
                   unsigned short WORD;                 /*  Word Access */
                   struct {                             /*  Byte Access */
                          unsigned char H;              /*    High      */
                          unsigned char L;              /*    Low       */
                          }       BYTE;                 /*              */
                   struct {                             /*  Bit  Access */
                          unsigned char B15:1;          /*    Bit 15    */
                          unsigned char B14:1;          /*    Bit 14    */
                          unsigned char B13:1;          /*    Bit 13    */
                          unsigned char B12:1;          /*    Bit 12    */
                          unsigned char B11:1;          /*    Bit 11    */
                          unsigned char B10:1;          /*    Bit 10    */
                          unsigned char B9 :1;          /*    Bit  9    */
                          unsigned char B8 :1;          /*    Bit  8    */
                          unsigned char B7 :1;          /*    Bit  7    */
                          unsigned char B6 :1;          /*    Bit  6    */
                          unsigned char B5 :1;          /*    Bit  5    */
                          unsigned char B4 :1;          /*    Bit  4    */
                          unsigned char B3 :1;          /*    Bit  3    */
                          unsigned char B2 :1;          /*    Bit  2    */
                          unsigned char B1 :1;          /*    Bit  1    */
                          unsigned char B0 :1;          /*    Bit  0    */
                          }       BIT;                  /*              */
                   }            DRL;                    /*              */
};                                                      /*              */
struct st_pb {                                          /* struct PB    */
             union {                                    /* PBDR         */
                   unsigned short WORD;                 /*  Word Access */
                   struct {                             /*  Byte Access */
                          unsigned char H;              /*    High      */
                          unsigned char L;              /*    Low       */
                          }       BYTE;                 /*              */
                   struct {                             /*  Bit  Access */
                          unsigned char   :8;           /*              */
                          unsigned char   :2;           /*              */
                          unsigned char B5:1;           /*    Bit 5     */
                          unsigned char B4:1;           /*    Bit 4     */
                          unsigned char B3:1;           /*    Bit 3     */
                          unsigned char B2:1;           /*    Bit 2     */
                          unsigned char B1:1;           /*    Bit 1     */
                          unsigned char B0:1;           /*    Bit 0     */
                          }       BIT;                  /*              */
                   }            DR;                     /*              */
};                                                      /*              */
struct st_pd {                                          /* struct PD    */
             union {                                    /* PDDRL        */
                   unsigned short WORD;                 /*  Word Access */
                   struct {                             /*  Byte Access */
                          unsigned char H;              /*    High      */
                          unsigned char L;              /*    Low       */
                          }       BYTE;                 /*              */
                   struct {                             /*  Bit  Access */
                          unsigned char   :7;           /*              */
                          unsigned char B8:1;           /*    Bit 8     */
                          unsigned char B7:1;           /*    Bit 7     */
                          unsigned char B6:1;           /*    Bit 6     */
                          unsigned char B5:1;           /*    Bit 5     */
                          unsigned char B4:1;           /*    Bit 4     */
                          unsigned char B3:1;           /*    Bit 3     */
                          unsigned char B2:1;           /*    Bit 2     */
                          unsigned char B1:1;           /*    Bit 1     */
                          unsigned char B0:1;           /*    Bit 0     */
                          }       BIT;                  /*              */
                   }            DRL;                    /*              */
};                                                      /*              */
struct st_pe {                                          /* struct PE    */
             union {                                    /* PEDRL        */
                   unsigned short WORD;                 /*  Word Access */
                   struct {                             /*  Byte Access */
                          unsigned char H;              /*    High      */
                          unsigned char L;              /*    Low       */
                          }       BYTE;                 /*              */
                   struct {                             /*  Bit  Access */
                          unsigned char B15:1;          /*    Bit 15    */
                          unsigned char B14:1;          /*    Bit 14    */
                          unsigned char B13:1;          /*    Bit 13    */
                          unsigned char B12:1;          /*    Bit 12    */
                          unsigned char B11:1;          /*    Bit 11    */
                          unsigned char B10:1;          /*    Bit 10    */
                          unsigned char B9 :1;          /*    Bit  9    */
                          unsigned char B8 :1;          /*    Bit  8    */
                          unsigned char B7 :1;          /*    Bit  7    */
                          unsigned char B6 :1;          /*    Bit  6    */
                          unsigned char B5 :1;          /*    Bit  5    */
                          unsigned char B4 :1;          /*    Bit  4    */
                          unsigned char B3 :1;          /*    Bit  3    */
                          unsigned char B2 :1;          /*    Bit  2    */
                          unsigned char B1 :1;          /*    Bit  1    */
                          unsigned char B0 :1;          /*    Bit  0    */
                          }       BIT;                  /*              */
                   }            DRL;                    /*              */
             char               wk[12];                 /*              */
             union {                                    /* PEDRH        */
                   unsigned short WORD;                 /*  Word Access */
                   struct {                             /*  Byte Access */
                          unsigned char H;              /*    High      */
                          unsigned char L;              /*    Low       */
                          }       BYTE;                 /*              */
                   struct {                             /*  Bit  Access */
                          unsigned char    :8;          /*              */
                          unsigned char    :2;          /*              */
                          unsigned char B21:1;          /*    Bit 21    */
                          unsigned char B20:1;          /*    Bit 20    */
                          unsigned char B19:1;          /*    Bit 19    */
                          unsigned char B18:1;          /*    Bit 18    */
                          unsigned char B17:1;          /*    Bit 17    */
                          unsigned char B16:1;          /*    Bit 16    */
                          }       BIT;                  /*              */
                   }            DRH;                    /*              */
};                                                      /*              */
struct st_pf {                                          /* struct PF    */
             union {                                    /* PFDR         */
                   unsigned short WORD;                 /*  Word Access */
                   struct {                             /*  Byte Access */
                          unsigned char H;              /*    High      */
                          unsigned char L;              /*    Low       */
                          }       BYTE;                 /*              */
                   struct {                             /*  Bit  Access */
                          unsigned char B15:1;          /*    Bit 15    */
                          unsigned char B14:1;          /*    Bit 14    */
                          unsigned char B13:1;          /*    Bit 13    */
                          unsigned char B12:1;          /*    Bit 12    */
                          unsigned char B11:1;          /*    Bit 11    */
                          unsigned char B10:1;          /*    Bit 10    */
                          unsigned char B9 :1;          /*    Bit  9    */
                          unsigned char B8 :1;          /*    Bit  8    */
                          unsigned char B7 :1;          /*    Bit  7    */
                          unsigned char B6 :1;          /*    Bit  6    */
                          unsigned char B5 :1;          /*    Bit  5    */
                          unsigned char B4 :1;          /*    Bit  4    */
                          unsigned char B3 :1;          /*    Bit  3    */
                          unsigned char B2 :1;          /*    Bit  2    */
                          unsigned char B1 :1;          /*    Bit  1    */
                          unsigned char B0 :1;          /*    Bit  0    */
                          }       BIT;                  /*              */
                   }            DR;                     /*              */
};                                                      /*              */
struct st_pfc {                                         /* struct PFC   */
              union {                                   /* PAIORL       */
                    unsigned short WORD;                /*  Word Access */
                    struct {                            /*  Byte Access */
                           unsigned char H;             /*    High      */
                           unsigned char L;             /*    Low       */
                           }       BYTE;                /*              */
                    struct {                            /*  Bit  Access */
                           unsigned char B15:1;         /*    Bit 15    */
                           unsigned char B14:1;         /*    Bit 14    */
                           unsigned char B13:1;         /*    Bit 13    */
                           unsigned char B12:1;         /*    Bit 12    */
                           unsigned char B11:1;         /*    Bit 11    */
                           unsigned char B10:1;         /*    Bit 10    */
                           unsigned char B9 :1;         /*    Bit  9    */
                           unsigned char B8 :1;         /*    Bit  8    */
                           unsigned char B7 :1;         /*    Bit  7    */
                           unsigned char B6 :1;         /*    Bit  6    */
                           unsigned char B5 :1;         /*    Bit  5    */
                           unsigned char B4 :1;         /*    Bit  4    */
                           unsigned char B3 :1;         /*    Bit  3    */
                           unsigned char B2 :1;         /*    Bit  2    */
                           unsigned char B1 :1;         /*    Bit  1    */
                           unsigned char B0 :1;         /*    Bit  0    */
                           }       BIT;                 /*              */
                    }           PAIORL;                 /*              */
              char              wk1[2];                 /*              */
              union {                                   /* PACRL3       */
                    unsigned short WORD;                /*  Word Access */
                    struct {                            /*  Byte Access */
                           unsigned char H;             /*    High      */
                           unsigned char L;             /*    Low       */
                           }       BYTE;                /*              */
                    struct {                            /*  Bit  Access */
                           unsigned char PA15MD:1;      /*    PA15MD    */
                           unsigned char PA14MD:1;      /*    PA14MD    */
                           unsigned char PA13MD:1;      /*    PA13MD    */
                           unsigned char PA12MD:1;      /*    PA12MD    */
                           unsigned char PA11MD:1;      /*    PA11MD    */
                           unsigned char PA10MD:1;      /*    PA10MD    */
                           unsigned char PA9MD :1;      /*    PA9MD     */
                           unsigned char PA8MD :1;      /*    PA8MD     */
                           unsigned char PA7MD :1;      /*    PA7MD     */
                           unsigned char PA6MD :1;      /*    PA6MD     */
                           unsigned char PA5MD :1;      /*    PA5MD     */
                           unsigned char PA4MD :1;      /*    PA4MD     */
                           unsigned char PA3MD :1;      /*    PA3MD     */
                           unsigned char PA2MD :1;      /*    PA2MD     */
                           unsigned char PA1MD :1;      /*    PA1MD     */
                           unsigned char PA0MD :1;      /*    PA0MD     */
                           }       BIT;                 /*              */
                    }           PACRL3;                 /*              */
              union {                                   /* PACRL1       */
                    unsigned short WORD;                /*  Word Access */
                    struct {                            /*  Byte Access */
                           unsigned char H;             /*    High      */
                           unsigned char L;             /*    Low       */
                           }       BYTE;                /*              */
                    struct {                            /*  Bit  Access */
                           unsigned char PA15MD:2;      /*    PA15MD    */
                           unsigned char PA14MD:2;      /*    PA14MD    */
                           unsigned char PA13MD:2;      /*    PA13MD    */
                           unsigned char PA12MD:2;      /*    PA12MD    */
                           unsigned char PA11MD:2;      /*    PA11MD    */
                           unsigned char PA10MD:2;      /*    PA10MD    */
                           unsigned char PA9MD :2;      /*    PA9MD     */
                           unsigned char PA8MD :2;      /*    PA8MD     */
                           }       BIT;                 /*              */
                    }           PACRL1;                 /*              */
              union {                                   /* PACRL2       */
                    unsigned short WORD;                /*  Word Access */
                    struct {                            /*  Byte Access */
                           unsigned char H;             /*    High      */
                           unsigned char L;             /*    Low       */
                           }       BYTE;                /*              */
                    struct {                            /*  Bit  Access */
                           unsigned char PA7MD:2;       /*    PA7MD     */
                           unsigned char PA6MD:2;       /*    PA6MD     */
                           unsigned char PA5MD:2;       /*    PA5MD     */
                           unsigned char PA4MD:2;       /*    PA4MD     */
                           unsigned char PA3MD:2;       /*    PA3MD     */
                           unsigned char PA2MD:2;       /*    PA2MD     */
                           unsigned char PA1MD:2;       /*    PA1MD     */
                           unsigned char PA0MD:2;       /*    PA0MD     */
                           }       BIT;                 /*              */
                    }           PACRL2;                 /*              */
              char              wk2[4];                 /*              */
              union {                                   /* PBIOR        */
                    unsigned short WORD;                /*  Word Access */
                    struct {                            /*  Byte Access */
                           unsigned char H;             /*    High      */
                           unsigned char L;             /*    Low       */
                           }       BYTE;                /*              */
                    struct {                            /*  Bit  Access */
                           unsigned char   :8;          /*              */
                           unsigned char   :2;          /*              */
                           unsigned char B5:1;          /*    Bit 5     */
                           unsigned char B4:1;          /*    Bit 4     */
                           unsigned char B3:1;          /*    Bit 3     */
                           unsigned char B2:1;          /*    Bit 2     */
                           unsigned char B1:1;          /*    Bit 1     */
                           unsigned char B0:1;          /*    Bit 0     */
                           }       BIT;                 /*              */
                    }           PBIOR;                  /*              */
              char              wk3[2];                 /*              */
              union {                                   /* PBCR1        */
                    unsigned short WORD;                /*  Word Access */
                    struct {                            /*  Byte Access */
                           unsigned char H;             /*    High      */
                           unsigned char L;             /*    Low       */
                           }       BYTE;                /*              */
                    struct {                            /*  Bit  Access */
                           unsigned char      :2;       /*              */
                           unsigned char PB5MD:1;       /*    PB5MD     */
                           unsigned char PB4MD:1;       /*    PB4MD     */
                           unsigned char PB3MD:1;       /*    PB3MD     */
                           unsigned char PB2MD:1;       /*    PB2MD     */
                           unsigned char PB1MD:1;       /*    PB1MD     */
                           }       BIT;                 /*              */
                    }           PBCR1;                  /*              */
              union {                                   /* PBCR2        */
                    unsigned short WORD;                /*  Word Access */
                    struct {                            /*  Byte Access */
                           unsigned char H;             /*    High      */
                           unsigned char L;             /*    Low       */
                           }       BYTE;                /*              */
                    struct {                            /*  Bit  Access */
                           unsigned char      :4;       /*              */
                           unsigned char PB5MD:2;       /*    PB5MD     */
                           unsigned char PB4MD:2;       /*    PB4MD     */
                           unsigned char PB3MD:2;       /*    PB3MD     */
                           unsigned char PB2MD:2;       /*    PB2MD     */
                           unsigned char PB1MD:2;       /*    PB1MD     */
                           unsigned char PB0MD:2;       /*    PB0MD     */
                           }       BIT;                 /*              */
                    }           PBCR2;                  /*              */
              char              wk4[10];                /*              */
              union {                                   /* PDIORL       */
                    unsigned short WORD;                /*  Word Access */
                    struct {                            /*  Byte Access */
                           unsigned char H;             /*    High      */
                           unsigned char L;             /*    Low       */
                           }       BYTE;                /*              */
                    struct {                            /*  Bit  Access */
                           unsigned char   :7;          /*              */
                           unsigned char B8:1;          /*    Bit 8     */
                           unsigned char B7:1;          /*    Bit 7     */
                           unsigned char B6:1;          /*    Bit 6     */
                           unsigned char B5:1;          /*    Bit 5     */
                           unsigned char B4:1;          /*    Bit 4     */
                           unsigned char B3:1;          /*    Bit 3     */
                           unsigned char B2:1;          /*    Bit 2     */
                           unsigned char B1:1;          /*    Bit 1     */
                           unsigned char B0:1;          /*    Bit 0     */
                           }       BIT;                 /*              */
                    }           PDIORL;                 /*              */
              char              wk5[4];                 /*              */
              union {                                   /* PDCRL1       */
                    unsigned short WORD;                /*  Word Access */
                    struct {                            /*  Byte Access */
                           unsigned char H;             /*    High      */
                           unsigned char L;             /*    Low       */
                           }       BYTE;                /*              */
                    struct {                            /*  Bit  Access */
                           unsigned char      :7;       /*              */
                           unsigned char PD8MD:1;       /*    PD8MD     */
                           unsigned char PD7MD:1;       /*    PD7MD     */
                           unsigned char PD6MD:1;       /*    PD6MD     */
                           unsigned char PD5MD:1;       /*    PD5MD     */
                           unsigned char PD4MD:1;       /*    PD4MD     */
                           unsigned char PD3MD:1;       /*    PD3MD     */
                           unsigned char PD2MD:1;       /*    PD2MD     */
                           unsigned char PD1MD:1;       /*    PD1MD     */
                           unsigned char PD0MD:1;       /*    PD0MD     */
                           }       BIT;                 /*              */
                    }           PDCRL1;                 /*              */
              union {                                   /* PDCRL2       */
                    unsigned short WORD;                /*  Word Access */
                    struct {                            /*  Byte Access */
                           unsigned char H;             /*    High      */
                           unsigned char L;             /*    Low       */
                           }       BYTE;                /*              */
                    struct {                            /*  Bit  Access */
                           unsigned char      :7;       /*              */
                           unsigned char PD8MD:1;       /*    PD8MD     */
                           unsigned char PD7MD:1;       /*    PD7MD     */
                           unsigned char PD6MD:1;       /*    PD6MD     */
                           unsigned char PD5MD:1;       /*    PD5MD     */
                           unsigned char PD4MD:1;       /*    PD4MD     */
                           unsigned char PD3MD:1;       /*    PD3MD     */
                           unsigned char PD2MD:1;       /*    PD2MD     */
                           unsigned char PD1MD:1;       /*    PD1MD     */
                           unsigned char PD0MD:1;       /*    PD0MD     */
                           }       BIT;                 /*              */
                    }           PDCRL2;                 /*              */
              char              wk6[4];                 /*              */
              union {                                   /* PEIORL       */
                    unsigned short WORD;                /*  Word Access */
                    struct {                            /*  Byte Access */
                           unsigned char H;             /*    High      */
                           unsigned char L;             /*    Low       */
                           }       BYTE;                /*              */
                    struct {                            /*  Bit  Access */
                           unsigned char B15:1;         /*    Bit 15    */
                           unsigned char B14:1;         /*    Bit 14    */
                           unsigned char B13:1;         /*    Bit 13    */
                           unsigned char B12:1;         /*    Bit 12    */
                           unsigned char B11:1;         /*    Bit 11    */
                           unsigned char B10:1;         /*    Bit 10    */
                           unsigned char B9 :1;         /*    Bit  9    */
                           unsigned char B8 :1;         /*    Bit  8    */
                           unsigned char B7 :1;         /*    Bit  7    */
                           unsigned char B6 :1;         /*    Bit  6    */
                           unsigned char B5 :1;         /*    Bit  5    */
                           unsigned char B4 :1;         /*    Bit  4    */
                           unsigned char B3 :1;         /*    Bit  3    */
                           unsigned char B2 :1;         /*    Bit  2    */
                           unsigned char B1 :1;         /*    Bit  1    */
                           unsigned char B0 :1;         /*    Bit  0    */
                           }       BIT;                 /*              */
                    }           PEIORL;                 /*              */
              union {                                   /* PEIORH       */
                    unsigned short WORD;                /*  Word Access */
                    struct {                            /*  Byte Access */
                           unsigned char H;             /*    High      */
                           unsigned char L;             /*    Low       */
                           }       BYTE;                /*              */
                    struct {                            /*  Bit  Access */
                           unsigned char    :8;         /*              */
                           unsigned char    :2;         /*              */
                           unsigned char B21:1;         /*    Bit 21    */
                           unsigned char B20:1;         /*    Bit 20    */
                           unsigned char B19:1;         /*    Bit 19    */
                           unsigned char B18:1;         /*    Bit 18    */
                           unsigned char B17:1;         /*    Bit 17    */
                           unsigned char B16:1;         /*    Bit 16    */
                           }       BIT;                 /*              */
                    }           PEIORH;                 /*              */
              union {                                   /* PECRL1       */
                    unsigned short WORD;                /*  Word Access */
                    struct {                            /*  Byte Access */
                           unsigned char H;             /*    High      */
                           unsigned char L;             /*    Low       */
                           }       BYTE;                /*              */
                    struct {                            /*  Bit  Access */
                           unsigned char PE15MD:2;      /*    PE15MD    */
                           unsigned char PE14MD:2;      /*    PE14MD    */
                           unsigned char PE13MD:2;      /*    PE13MD    */
                           unsigned char PE12MD:2;      /*    PE12MD    */
                           unsigned char PE11MD:2;      /*    PE11MD    */
                           unsigned char PE10MD:2;      /*    PE10MD    */
                           unsigned char PE9MD :2;      /*    PE9MD     */
                           unsigned char PE8MD :2;      /*    PE8MD     */
                           }       BIT;                 /*              */
                    }           PECRL1;                 /*              */
              union {                                   /* PECRL2       */
                    unsigned short WORD;                /*  Word Access */
                    struct {                            /*  Byte Access */
                           unsigned char H;             /*    High      */
                           unsigned char L;             /*    Low       */
                           }       BYTE;                /*              */
                    struct {                            /*  Bit  Access */
                           unsigned char PE7MD:2;       /*    PE7MD     */
                           unsigned char PE6MD:2;       /*    PE6MD     */
                           unsigned char PE5MD:2;       /*    PE5MD     */
                           unsigned char PE4MD:2;       /*    PE4MD     */
                           unsigned char PE3MD:2;       /*    PE3MD     */
                           unsigned char PE2MD:2;       /*    PE2MD     */
                           unsigned char PE1MD:2;       /*    PE1MD     */
                           unsigned char PE0MD:2;       /*    PE0MD     */
                           }       BIT;                 /*              */
                    }           PECRL2;                 /*              */
              union {                                   /* PECRH        */
                    unsigned short WORD;                /*  Word Access */
                    struct {                            /*  Byte Access */
                           unsigned char H;             /*    High      */
                           unsigned char L;             /*    Low       */
                           }       BYTE;                /*              */
                    struct {                            /*  Bit  Access */
                           unsigned char       :4;      /*              */
                           unsigned char PE21MD:2;      /*    PE21MD    */
                           unsigned char PE20MD:2;      /*    PE20MD    */
                           unsigned char PE19MD:2;      /*    PE19MD    */
                           unsigned char PE18MD:2;      /*    PE18MD    */
                           unsigned char PE17MD:2;      /*    PE17MD    */
                           unsigned char PE16MD:2;      /*    PE16MD    */
                           }       BIT;                 /*              */
                    }           PECRH;                  /*              */
};                                                      /*              */
struct st_cmt {                                         /* struct CMT   */
              union {                                   /* CMSTR        */
                    unsigned short WORD;                /*  Word Access */
                    struct {                            /*  Bit  Access */
                           unsigned char     :8;        /*              */
                           unsigned char     :6;        /*              */
                           unsigned char STR1:1;        /*    STR1      */
                           unsigned char STR0:1;        /*    STR0      */
                           }       BIT;                 /*              */
                    }           CMSTR;                  /*              */
};                                                      /*              */
struct st_cmt0 {                                        /* struct CMT0  */
               union {                                  /* CMCSR        */
                     unsigned short WORD;               /*  Word Access */
                     struct {                           /*  Byte Access */
                            unsigned char     :8;       /*              */
                            unsigned char CMF :1;       /*    CMF       */
                            unsigned char CMIE:1;       /*    CMIE      */
                            unsigned char     :4;       /*              */
                            unsigned char CKS :2;       /*    CKS       */
                            }       BIT;                /*              */
                     }          CMCSR;                  /*              */
               unsigned short   CMCNT;                  /* CMCNT        */
               unsigned short   CMCOR;                  /* CMCOR        */
};                                                      /*              */
struct st_ad0 {                                         /* struct A/D0  */
              union {                                   /* ADDR0        */
                    unsigned short WORD;                /*  Word Access */
                    unsigned char  BYTE;                /*  Byte Access */
                    }           ADDR0;                  /*              */
              union {                                   /* ADDR1        */
                    unsigned short WORD;                /*  Word Access */
                    unsigned char  BYTE;                /*  Byte Access */
                    }           ADDR1;                  /*              */
              union {                                   /* ADDR2        */
                    unsigned short WORD;                /*  Word Access */
                    unsigned char  BYTE;                /*  Byte Access */
                    }           ADDR2;                  /*              */
              union {                                   /* ADDR3        */
                    unsigned short WORD;                /*  Word Access */
                    unsigned char  BYTE;                /*  Byte Access */
                    }           ADDR3;                  /*              */
              char              wk1[8];                 /*              */
              union {                                   /* ADDR8        */
                    unsigned short WORD;                /*  Word Access */
                    unsigned char  BYTE;                /*  Byte Access */
                    }           ADDR8;                  /*              */
              union {                                   /* ADDR9        */
                    unsigned short WORD;                /*  Word Access */
                    unsigned char  BYTE;                /*  Byte Access */
                    }           ADDR9;                  /*              */
              union {                                   /* ADDR10       */
                    unsigned short WORD;                /*  Word Access */
                    unsigned char  BYTE;                /*  Byte Access */
                    }           ADDR10;                 /*              */
              union {                                   /* ADDR11       */
                    unsigned short WORD;                /*  Word Access */
                    unsigned char  BYTE;                /*  Byte Access */
                    }           ADDR11;                 /*              */
              char              wk2[72];                /*              */
              union {                                   /* ADCSR        */
                    unsigned char BYTE;                 /*  Byte Access */
                    struct {                            /*  Bit  Access */
                           unsigned char ADF :1;        /*    ADF       */
                           unsigned char ADIE:1;        /*    ADIE      */
                           unsigned char ADM :2;        /*    ADM       */
                           unsigned char     :1;        /*              */
                           unsigned char CH  :3;        /*    CH        */
                           }      BIT;                  /*              */
                    }           ADCSR;                  /*              */
              char              wk3[7];                 /*              */
              union {                                   /* ADCR         */
                    unsigned char BYTE;                 /*  Byte Access */
                    struct {                            /*  Bit  Access */
                           unsigned char TRGE:1;        /*    TRGE      */
                           unsigned char CKS :2;        /*    CKS       */
                           unsigned char ADST:1;        /*    ADST      */
                           unsigned char ADCS:1;        /*    ADCS      */
                           }      BIT;                  /*              */
                    }           ADCR;                   /*              */
              char              wk4[875];               /*              */
              union {                                   /* ADTSR        */
                    unsigned char BYTE;                 /*  Byte Access */
                    struct {                            /*  Bit  Access */
                           unsigned char     :6;        /*              */
                           unsigned char TRGS:2;        /*    TRGS      */
                           }      BIT;                  /*              */
                    }            ADTSR;                 /*              */
};                                                      /*              */
struct st_ad1 {                                         /* struct A/D1  */
              union {                                   /* ADDR4        */
                    unsigned short WORD;                /*  Word Access */
                    unsigned char  BYTE;                /*  Byte Access */
                    }           ADDR4;                  /*              */
              union {                                   /* ADDR5        */
                    unsigned short WORD;                /*  Word Access */
                    unsigned char  BYTE;                /*  Byte Access */
                    }           ADDR5;                  /*              */
              union {                                   /* ADDR6        */
                    unsigned short WORD;                /*  Word Access */
                    unsigned char  BYTE;                /*  Byte Access */
                    }           ADDR6;                  /*              */
              union {                                   /* ADDR7        */
                    unsigned short WORD;                /*  Word Access */
                    unsigned char  BYTE;                /*  Byte Access */
                    }           ADDR7;                  /*              */
              char              wk1[8];                 /*              */
              union {                                   /* ADDR12       */
                    unsigned short WORD;                /*  Word Access */
                    unsigned char  BYTE;                /*  Byte Access */
                    }           ADDR12;                 /*              */
              union {                                   /* ADDR13       */
                    unsigned short WORD;                /*  Word Access */
                    unsigned char  BYTE;                /*  Byte Access */
                    }           ADDR13;                 /*              */
              union {                                   /* ADDR14       */
                    unsigned short WORD;                /*  Word Access */
                    unsigned char  BYTE;                /*  Byte Access */
                    }           ADDR14;                 /*              */
              union {                                   /* ADDR15       */
                    unsigned short WORD;                /*  Word Access */
                    unsigned char  BYTE;                /*  Byte Access */
                    }           ADDR15;                 /*              */
              char              wk2[65];                /*              */
              union {                                   /* ADCSR        */
                    unsigned char BYTE;                 /*  Byte Access */
                    struct {                            /*  Bit  Access */
                           unsigned char ADF :1;        /*    ADF       */
                           unsigned char ADIE:1;        /*    ADIE      */
                           unsigned char ADM :2;        /*    ADM       */
                           unsigned char     :1;        /*              */
                           unsigned char CH  :3;        /*    CH        */
                           }      BIT;                  /*              */
                    }           ADCSR;                  /*              */
              char              wk3[7];                 /*              */
              union {                                   /* ADCR         */
                    unsigned char BYTE;                 /*  Byte Access */
                    struct {                            /*  Bit  Access */
                           unsigned char TRGE:1;        /*    TRGE      */
                           unsigned char CKS :2;        /*    CKS       */
                           unsigned char ADST:1;        /*    ADST      */
                           unsigned char ADCS:1;        /*    ADCS      */
                           }      BIT;                  /*              */
                    }            ADCR;                  /*              */
              char              wk4[874];               /*              */
              union {                                   /* ADTSR        */
                    unsigned char BYTE;                 /*  Byte Access */
                    struct {                            /*  Bit  Access */
                           unsigned char     :4;        /*              */
                           unsigned char TRGS:2;        /*    TRGS      */
                           }      BIT;                  /*              */
                    }            ADTSR;                 /*              */
};                                                      /*              */
struct st_flash {                                       /* struct FLASH */
                union {                                 /* FLMCR1       */
                      unsigned char BYTE;               /*  Byte Access */
                      struct {                          /*  Bit  Access */
                             unsigned char FWE:1;       /*    FWE       */
                             unsigned char SWE:1;       /*    SWE       */
                             unsigned char ESU:1;       /*    ESU       */
                             unsigned char PSU:1;       /*    PSU       */
                             unsigned char EV :1;       /*    EV        */
                             unsigned char PV :1;       /*    PV        */
                             unsigned char E  :1;       /*    E         */
                             unsigned char P  :1;       /*    P         */
                             }      BIT;                /*              */
                      }         FLMCR1;                 /*              */
                union {                                 /* FLMCR2       */
                      unsigned char BYTE;               /*  Byte Access */
                      struct {                          /*  Bit  Access */
                             unsigned char FLER:1;      /*    FLER      */
                             }      BIT;                /*              */
                      }         FLMCR2;                 /*              */
                union {                                 /* EBR1         */
                      unsigned char BYTE;               /*  Byte Access */
                      struct {                          /*  Bit  Access */
                             unsigned char EB7:1;       /*    EB7       */
                             unsigned char EB6:1;       /*    EB6       */
                             unsigned char EB5:1;       /*    EB5       */
                             unsigned char EB4:1;       /*    EB4       */
                             unsigned char EB3:1;       /*    EB3       */
                             unsigned char EB2:1;       /*    EB2       */
                             unsigned char EB1:1;       /*    EB1       */
                             unsigned char EB0:1;       /*    EB0       */
                             }      BIT;                /*              */
                      }         EBR1;                   /*              */
                union {                                 /* EBR2         */
                      unsigned char BYTE;               /*  Byte Access */
                      struct {                          /*  Bit  Access */
                             unsigned char     :4;      /*              */
                             unsigned char EB11:1;      /*    EB11      */
                             unsigned char EB10:1;      /*    EB10      */
                             unsigned char EB9 :1;      /*    EB9       */
                             unsigned char EB8 :1;      /*    EB8       */
                             }      BIT;                /*              */
                      }         EBR2;                   /*              */
                char            wk[165];                /*              */
                union {                                 /* RAMER        */
                      unsigned char BYTE;               /*  Byte Access */
                      struct {                          /*  Bit  Access */
                             unsigned char     :4;      /*              */
                             unsigned char RAMS:1;      /*    RAMS      */
                             unsigned char RAM :3;      /*    RAM       */
                             }      BIT;                /*              */
                      }         RAMER;                  /*              */
};                                                      /*              */
struct st_ubc {                                         /* struct UBC   */
              void             *UBAR;                   /* UBAR         */
              unsigned int      UBAMR;                  /* UBAMR        */
              union {                                   /* UBBR         */
                    unsigned short WORD;                /*  Word Access */
                    struct {                            /*  Bit  Access */
                           unsigned char   :8;          /*              */
                           unsigned char CP:2;          /*    CP        */
                           unsigned char ID:2;          /*    ID        */
                           unsigned char RW:2;          /*    RW        */
                           unsigned char SZ:2;          /*    SZ        */
                           }       BIT;                 /*              */
                    }           UBBR;                   /*              */
              union {                                   /* UBCR         */
                    unsigned short WORD;                /*  Word Access */
                    struct {                            /*  Bit  Access */
                           unsigned char     :8;        /*              */
                           unsigned char     :5;        /*              */
                           unsigned char CKS :2;        /*    CKS       */
                           unsigned char UBID:1;        /*    UBID      */
                           }       BIT;                 /*              */
                    }           UBCR;                   /*              */
};                                                      /*              */
union un_wdt {                                          /* union WDT    */
             struct {                                   /* Read  Access */
                    union {                             /* TCSR         */
                          unsigned char BYTE;           /*  Byte Access */
                          struct {                      /*  Bit  Access */
                                 unsigned char OVF :1;  /*    OVF       */
                                 unsigned char WTIT:1;  /*    WT/IT     */
                                 unsigned char TME :1;  /*    TME       */
                                 unsigned char     :2;  /*              */
                                 unsigned char CKS :3;  /*    CKS       */
                                 }      BIT;            /*              */
                          }       TCSR;                 /*              */
                    unsigned char TCNT;                 /* TCNT         */
                    char          wk;                   /*              */
                    union {                             /* RSTCSR       */
                          unsigned char BYTE;           /*  Byte Access */
                          struct {                      /*              */
                                 unsigned char WRST:1;  /*    WSRT      */
                                 unsigned char RSTE:1;  /*    RSTE      */
                                 unsigned char RSTS:1;  /*    RSTS      */
                                 }      BIT;            /*              */
                          }       RSTCSR;               /*              */
                    } READ;                             /*              */
             struct {                                   /* Write Access */
                    unsigned short TCSR;                /* TCSR/TCNT    */
                    unsigned short RSTCSR;              /* RSTCSR       */
                    } WRITE;                            /*              */
};                                                      /*              */
union un_sbycr {                                        /* union SBYCR  */
               unsigned char BYTE;                      /*  Byte Access */
               struct {                                 /*  Bit  Access */
                      unsigned char SSBY :1;            /*    SSBY      */
                      unsigned char HIZ  :1;            /*    HIZ       */
                      unsigned char      :5;            /*              */
                      unsigned char IRQEL:1;            /*    IRQEL     */
                      }      BIT;                       /*              */
};                                                      /*              */
union un_syscr {                                        /* union SYSCR  */
               unsigned char BYTE;                      /*  Byte Access */
               struct {                                 /*  Bit  Access */
                      unsigned char        :6;          /*              */
                      unsigned char AUDSRST:1;          /*    AUDSRST   */
                      unsigned char RAME   :1;          /*    RAME      */
                      }      BIT;                       /*              */
};                                                      /*              */
struct st_mst {                                         /* struct MST   */
              union {                                   /* CR1          */
                    unsigned short WORD;                /*  Word Access */
                    struct {                            /*  Bit  Access */
                           unsigned char      :4;       /*              */
                           unsigned char _RAM :1;       /*    RAM       */
                           unsigned char _ROM :1;       /*    ROM       */
                           unsigned char _DTC :2;       /*    DTC       */
                           unsigned char      :3;       /*              */
                           unsigned char _SCI4:1;       /*    SCI4      */
                           unsigned char _SCI3:1;       /*    SCI3      */
                           unsigned char _SCI2:1;       /*    SCI2      */
                           }       BIT;                 /*              */
                    }           CR1;                    /*              */
              union {                                   /* CR2          */
                    unsigned short WORD;                /*  Word Access */
                    struct {                            /*  Bit  Access */
                           unsigned char       :1;      /*              */
                           unsigned char _MMT  :1;      /*    MMT       */
                           unsigned char _MTU  :1;      /*    MTU       */
                           unsigned char _CMT  :1;      /*    CMT       */
                           unsigned char       :2;      /*              */
                           unsigned char _HCAN2:1;      /*    HCAN2     */
                           unsigned char       :1;      /*              */
                           unsigned char       :2;      /*              */
                           unsigned char _AD1  :1;      /*    A/D1      */
                           unsigned char _AD0  :1;      /*    A/D0      */
                           unsigned char _AUD  :1;      /*    AUD       */
                           unsigned char _HUDI :1;      /*    H-UDI     */
                           unsigned char       :1;      /*              */
                           unsigned char _UBC  :1;      /*    UBC       */
                           }       BIT;                 /*              */
                    }           CR2;                    /*              */
};                                                      /*              */
struct st_bsc {                                         /* struct BSC   */
              union {                                   /* BCR1         */
                    unsigned short WORD;                /*  Word Access */
                    struct {                            /*  Bit  Access */
                           unsigned char       :1;      /*              */
                           unsigned char MMTRWE:1;      /*    MMTRWE    */
                           unsigned char MTURWE:1;      /*    MTURWE    */
                           unsigned char       :5;      /*              */
                           unsigned char       :7;      /*              */
                           unsigned char A0SZ  :1;      /*    A0SZ      */
                           }       BIT;                 /*              */
                    }           BCR1;                   /*              */
              union {                                   /* BCR2         */
                    unsigned short WORD;                /*  Word Access */
                    struct {                            /*  Bit  Access */
                           unsigned char    :6;         /*              */
                           unsigned char IW0:2;         /*    IW0       */
                           unsigned char    :3;         /*              */
                           unsigned char CW0:1;         /*    CW0       */
                           unsigned char    :3;         /*              */
                           unsigned char SW0:1;         /*    SW0       */
                           }       BIT;                 /*              */
                    }           BCR2;                   /*              */
              union {                                   /* WCR1         */
                    unsigned short WORD;                /*  Word Access */
                    struct {                            /*  Bit  Access */
                           unsigned char   :8;          /*              */
                           unsigned char   :4;          /*              */
                           unsigned char W0:4;          /*    W0        */
                           }       BIT;                 /*              */
                    }           WCR1;                   /*              */
};                                                      /*              */
struct st_dtc {                                         /* struct DTC   */
              union {                                   /* DTEA         */
                    unsigned char BYTE;                 /*  Byte Access */
                    struct {                            /*  Bit  Access */
                           unsigned char TGI4A:1;       /*    TGI4A     */
                           unsigned char TGI4B:1;       /*    TGI4B     */
                           unsigned char TGI4C:1;       /*    TGI4C     */
                           unsigned char TGI4D:1;       /*    TGI4D     */
                           unsigned char TGI4V:1;       /*    TGI4V     */
                           unsigned char TGI3A:1;       /*    TGI3A     */
                           unsigned char TGI3B:1;       /*    TGI3B     */
                           unsigned char TGI3C:1;       /*    TGI3C     */
                           }      BIT;                  /*              */
                    }           DTEA;                   /*              */
              union {                                   /* DTEB         */
                    unsigned char BYTE;                 /*  Byte Access */
                    struct {                            /*  Bit  Access */
                           unsigned char TGI3D:1;       /*    TGI3D     */
                           unsigned char TGI2A:1;       /*    TGI2A     */
                           unsigned char TGI2B:1;       /*    TGI2B     */
                           unsigned char TGI1A:1;       /*    TGI1A     */
                           unsigned char TGI1B:1;       /*    TGI1B     */
                           unsigned char TGI0A:1;       /*    TGI0A     */
                           unsigned char TGI0B:1;       /*    TGI0B     */
                           unsigned char TGI0C:1;       /*    TGI0C     */
                           }      BIT;                  /*              */
                    }           DTEB;                   /*              */
              union {                                   /* DTEC         */
                    unsigned char BYTE;                 /*  Byte Access */
                    struct {                            /*  Bit  Access */
                           unsigned char TGI0D:1;       /*    TGI0D     */
                           unsigned char ADI0 :1;       /*    ADI0      */
                           unsigned char IRQ0 :1;       /*    IRQ0      */
                           unsigned char IRQ1 :1;       /*    IRQ1      */
                           unsigned char IRQ2 :1;       /*    IRQ2      */
                           unsigned char IRQ3 :1;       /*    IRQ3      */
                           }      BIT;                  /*              */
                    }           DTEC;                   /*              */
              union {                                   /* DTED         */
                    unsigned char BYTE;                 /*  Byte Access */
                    struct {                            /*  Bit  Access */
                           unsigned char     :2;        /*              */
                           unsigned char CMI0:1;        /*    CMI0      */
                           unsigned char CMI1:1;        /*    CMI1      */
                           }      BIT;                  /*              */
                    }           DTED;                   /*              */
              char              wk1[2];                 /*              */
              union {                                   /* DTCSR        */
                    unsigned short WORD;                /*  Word Access */
                    struct {                            /*  Bit  Access */
                           unsigned char      :5;       /*              */
                           unsigned char NMIF :1;       /*    NMIF      */
                           unsigned char AE   :1;       /*    AE        */
                           unsigned char SWDTE:1;       /*    SWDTE     */
                           unsigned char DTVEC:8;       /*    DTVEC     */
                           }       BIT;                 /*              */
                    }           DTCSR;                  /*              */
              unsigned short    DTBR;                   /* DTBR         */
              char              wk2[6];                 /*              */
              union {                                   /* DTEE         */
                    unsigned char BYTE;                 /*  Byte Access */
                    struct {                            /*  Bit  Access */
                           unsigned char     :2;        /*              */
                           unsigned char ADI1:1;        /*    ADI1      */
                           unsigned char     :1;        /*              */
                           unsigned char RXI2:1;        /*    RXI2      */
                           unsigned char TXI2:1;        /*    TXI2      */
                           unsigned char RXI3:1;        /*    RXI3      */
                           unsigned char TXI3:1;        /*    TXI3      */
                           }      BIT;                  /*              */
                    }           DTEE;                   /*              */
              union {                                   /* DTEF         */
                    unsigned char BYTE;                 /*  Byte Access */
                    struct {                            /*  Bit  Access */
                           unsigned char RXI4:1;        /*    RXI4      */
                           unsigned char TXI4:1;        /*    TXI4      */
                           unsigned char TGN :1;        /*    TGN       */
                           unsigned char TGM :1;        /*    TGM       */
                           unsigned char     :1;        /*              */
                           unsigned char RM1 :1;        /*    RM1       */
                           }      BIT;                  /*              */
                    }           DTEF;                   /*              */
};                                                      /*              */
struct st_mmt {                                         /* struct MMT   */
              union {                                   /* TMDR         */
                    unsigned char BYTE;                 /*  Byte Access */
                    struct {                            /*  Bit  Access */
                           unsigned char CKS :4;        /*    CKS       */
                           unsigned char OLSN:1;        /*    OLSN      */
                           unsigned char OLSP:1;        /*    OLSP      */
                           unsigned char MD  :2;        /*    MD        */
                           }      BIT;                  /*              */
                    }           TMDR;                   /*              */
              char              wk1;                    /*              */
              union {                                   /* TCNR         */
                    unsigned char BYTE;                 /*  Byte Access */
                    struct {                            /*  Bit  Access */
                           unsigned char TTGE :1;       /*    TTGE      */
                           unsigned char CST  :1;       /*    CST       */
                           unsigned char RPRO :1;       /*    RPRO      */
                           unsigned char      :3;       /*              */
                           unsigned char TGIEN:1;       /*    TGIEN     */
                           unsigned char TGIEM:1;       /*    TGIEM     */
                           }      BIT;                  /*              */
                    }           TCNR;                   /*              */
              char              wk2;                    /*              */
              union {                                   /* TSR          */
                    unsigned char BYTE;                 /*  Byte Access */
                    struct {                            /*  Bit  Access */
                           unsigned char TCFD:1;        /*    TCFD      */
                           unsigned char     :5;        /*              */
                           unsigned char TGFN:1;        /*    TGFN      */
                           unsigned char TGFM:1;        /*    TGFM      */
                           }      BIT;                  /*              */
                    }           TSR;                    /*              */
              char              wk3;                    /*              */
              unsigned short    TCNT;                   /* TCNT         */
              unsigned short    TPDR;                   /* TPDR         */
              unsigned short    TPBR;                   /* TPBR         */
              unsigned short    TDDR;                   /* TDDR         */
              char              wk4[2];                 /*              */
              unsigned short    TBRU;                   /* TBRU         */
              unsigned short    TGRUU;                  /* TGRUU        */
              unsigned short    TGRU;                   /* TGRU         */
              unsigned short    TGRUD;                  /* TGRUD        */
              unsigned short    TDCNT0;                 /* TDCNT0       */
              unsigned short    TDCNT1;                 /* TDCNT1       */
              unsigned short    TBRUF;                  /* TBRU(Free)   */
              char              wk5[2];                 /*              */
              unsigned short    TBRV;                   /* TBRV         */
              unsigned short    TGRVU;                  /* TGRVU        */
              unsigned short    TGRV;                   /* TGRV         */
              unsigned short    TGRVD;                  /* TGRVD        */
              unsigned short    TDCNT2;                 /* TDCNT2       */
              unsigned short    TDCNT3;                 /* TDCNT3       */
              unsigned short    TBRVF;                  /* TBRV(Free)   */
              char              wk6[2];                 /*              */
              unsigned short    TBRW;                   /* TBRW         */
              unsigned short    TGRWU;                  /* TGRWU        */
              unsigned short    TGRW;                   /* TGRW         */
              unsigned short    TGRWD;                  /* TGRWD        */
              unsigned short    TDCNT4;                 /* TDCNT4       */
              unsigned short    TDCNT5;                 /* TDCNT5       */
              unsigned short    TBRWF;                  /* TBRW(Free)   */
};                                                      /*              */
struct st_pwm {                                         /* struct PWM   */
              union {                                   /* TMDR         */
                    unsigned char BYTE;                 /*  Byte Access */
                    struct {                            /*  Bit  Access */
                           unsigned char CKS :4;        /*    CKS       */
                           unsigned char OLSN:1;        /*    OLSN      */
                           unsigned char OLSP:1;        /*    OLSP      */
                           unsigned char MD  :2;        /*    MD        */
                           }      BIT;                  /*              */
                    }           TMDR;                   /*              */
              char              wk1;                    /*              */
              union {                                   /* TCNR         */
                    unsigned char BYTE;                 /*  Byte Access */
                    struct {                            /*  Bit  Access */
                           unsigned char TTGE :1;       /*    TTGE      */
                           unsigned char CST  :1;       /*    CST       */
                           unsigned char RPRO :1;       /*    RPRO      */
                           unsigned char      :3;       /*              */
                           unsigned char TGIEN:1;       /*    TGIEN     */
                           unsigned char TGIEM:1;       /*    TGIEM     */
                           }      BIT;                  /*              */
                    }           TCNR;                   /*              */
              char              wk2;                    /*              */
              union {                                   /* TSR          */
                    unsigned char BYTE;                 /*  Byte Access */
                    struct {                            /*  Bit  Access */
                           unsigned char TCFD:1;        /*    TCFD      */
                           unsigned char     :5;        /*              */
                           unsigned char TGFN:1;        /*    TGFN      */
                           unsigned char TGFM:1;        /*    TGFM      */
                           }      BIT;                  /*              */
                    }           TSR;                    /*              */
              char              wk3;                    /*              */
              unsigned short    TCNT;                   /* TCNT         */
              unsigned short    TPDR;                   /* TPDR         */
              unsigned short    TPBR;                   /* TPBR         */
              unsigned short    TDDR;                   /* TDDR         */
};                                                      /*              */
struct st_pwmu {                                        /* struct PWMU  */
               unsigned short    TBRU;                  /* TBRU         */
               unsigned short    TGRUU;                 /* TGRUU        */
               unsigned short    TGRU;                  /* TGRU         */
               unsigned short    TGRUD;                 /* TGRUD        */
               unsigned short    TDCNT0;                /* TDCNT0       */
               unsigned short    TDCNT1;                /* TDCNT1       */
               unsigned short    TBRUF;                 /* TBRU(Free)   */
};                                                      /*              */
struct st_pwmv {                                        /* struct PWMV  */
               unsigned short    TBRV;                  /* TBRV         */
               unsigned short    TGRVU;                 /* TGRVU        */
               unsigned short    TGRV;                  /* TGRV         */
               unsigned short    TGRVD;                 /* TGRVD        */
               unsigned short    TDCNT2;                /* TDCNT2       */
               unsigned short    TDCNT3;                /* TDCNT3       */
               unsigned short    TBRVF;                 /* TBRV(Free)   */
};                                                      /*              */
struct st_pwmw {                                        /* struct PWMV  */
               unsigned short    TBRW;                  /* TBRW         */
               unsigned short    TGRWU;                 /* TGRWU        */
               unsigned short    TGRW;                  /* TGRW         */
               unsigned short    TGRWD;                 /* TGRWD        */
               unsigned short    TDCNT4;                /* TDCNT4       */
               unsigned short    TDCNT5;                /* TDCNT5       */
               unsigned short    TBRWF;                 /* TBRW(Free)   */
};                                                      /*              */
struct st_hudi {                                        /* struct H-UDI */
               union {                                  /* SDIR         */
                     unsigned short WORD;               /*  Word Access */
                     struct {                           /*  Bit Access  */
                            unsigned char TS:4;         /*    TS        */
                            }       BIT;                /*              */
                     }          SDIR;                   /*              */
               union {                                  /* SDSR         */
                     unsigned short WORD;               /*  Word Access */
                     struct {                           /*  Bit Access  */
                            unsigned char      :8;      /*              */
                            unsigned char      :7;      /*              */
                            unsigned char SDTRF:1;      /*    SDTRF     */
                            }       BIT;                /*              */
                      }         SDSR;                   /*              */
               unsigned int     SDDR;                   /* SDDR         */
};                                                      /*              */
union un_mb31_0 {                                       /* MB31-MB0     */
                unsigned int LONG;                      /*  Long Access */
                struct {                                /*  Bit  Access */
                       unsigned char MB31:1;            /*    MB31      */
                       unsigned char MB30:1;            /*    MB30      */
                       unsigned char MB29:1;            /*    MB29      */
                       unsigned char MB28:1;            /*    MB28      */
                       unsigned char MB27:1;            /*    MB27      */
                       unsigned char MB26:1;            /*    MB26      */
                       unsigned char MB25:1;            /*    MB25      */
                       unsigned char MB24:1;            /*    MB24      */
                       unsigned char MB23:1;            /*    MB23      */
                       unsigned char MB22:1;            /*    MB22      */
                       unsigned char MB21:1;            /*    MB21      */
                       unsigned char MB20:1;            /*    MB20      */
                       unsigned char MB19:1;            /*    MB19      */
                       unsigned char MB18:1;            /*    MB18      */
                       unsigned char MB17:1;            /*    MB17      */
                       unsigned char MB16:1;            /*    MB16      */
                       unsigned char MB15:1;            /*    MB15      */
                       unsigned char MB14:1;            /*    MB14      */
                       unsigned char MB13:1;            /*    MB13      */
                       unsigned char MB12:1;            /*    MB12      */
                       unsigned char MB11:1;            /*    MB11      */
                       unsigned char MB10:1;            /*    MB10      */
                       unsigned char MB9 :1;            /*    MB9       */
                       unsigned char MB8 :1;            /*    MB8       */
                       unsigned char MB7 :1;            /*    MB7       */
                       unsigned char MB6 :1;            /*    MB6       */
                       unsigned char MB5 :1;            /*    MB5       */
                       unsigned char MB4 :1;            /*    MB4       */
                       unsigned char MB3 :1;            /*    MB3       */
                       unsigned char MB2 :1;            /*    MB2       */
                       unsigned char MB1 :1;            /*    MB1       */
                       unsigned char MB0 :1;            /*    MB0       */
                       }     BIT;                       /*              */
};                                                      /*              */
union un_mb31_1 {                                       /* MB31-MB1     */
                unsigned int LONG;                      /*  Long Access */
                struct {                                /*  Bit  Access */
                       unsigned char MB31:1;            /*    MB31      */
                       unsigned char MB30:1;            /*    MB30      */
                       unsigned char MB29:1;            /*    MB29      */
                       unsigned char MB28:1;            /*    MB28      */
                       unsigned char MB27:1;            /*    MB27      */
                       unsigned char MB26:1;            /*    MB26      */
                       unsigned char MB25:1;            /*    MB25      */
                       unsigned char MB24:1;            /*    MB24      */
                       unsigned char MB23:1;            /*    MB23      */
                       unsigned char MB22:1;            /*    MB22      */
                       unsigned char MB21:1;            /*    MB21      */
                       unsigned char MB20:1;            /*    MB20      */
                       unsigned char MB19:1;            /*    MB19      */
                       unsigned char MB18:1;            /*    MB18      */
                       unsigned char MB17:1;            /*    MB17      */
                       unsigned char MB16:1;            /*    MB16      */
                       unsigned char MB15:1;            /*    MB15      */
                       unsigned char MB14:1;            /*    MB14      */
                       unsigned char MB13:1;            /*    MB13      */
                       unsigned char MB12:1;            /*    MB12      */
                       unsigned char MB11:1;            /*    MB11      */
                       unsigned char MB10:1;            /*    MB10      */
                       unsigned char MB9 :1;            /*    MB9       */
                       unsigned char MB8 :1;            /*    MB8       */
                       unsigned char MB7 :1;            /*    MB7       */
                       unsigned char MB6 :1;            /*    MB6       */
                       unsigned char MB5 :1;            /*    MB5       */
                       unsigned char MB4 :1;            /*    MB4       */
                       unsigned char MB3 :1;            /*    MB3       */
                       unsigned char MB2 :1;            /*    MB2       */
                       unsigned char MB1 :1;            /*    MB1       */
                       }     BIT;                       /*              */
};                                                      /*              */
struct st_hcan2 {                                       /* struct HCAN2 */
                union {                                 /* MCR          */
                      unsigned short WORD;              /*  Word Access */
                      struct {                          /*  Bit  Access */
                             unsigned char      :8;     /*              */
                             unsigned char MCR6 :1;     /*    SLPME     */
                             unsigned char      :1;     /*              */
                             unsigned char MCR5 :1;     /*    SLPM      */
                             unsigned char      :2;     /*              */
                             unsigned char MCR2  :1;     /*    MSM       */
                             unsigned char MCR1 :1;     /*    HALT      */
                             unsigned char MCR0  :1;     /*    RST       */
                             }       BIT;               /*              */
                      }         MCR;                    /*              */
                union {                                 /* GSR          */
                      unsigned short WORD;              /*  Word Access */
                      struct {                          /*  Bit  Access */
                             unsigned char     :8;      /*              */
                             unsigned char     :2;      /*              */
                             unsigned char GSR5:1;      /*    EPSB      */
                             unsigned char GSR4:1;      /*    HSB       */
                             unsigned char GSR3:1;      /*    RSB       */
                             unsigned char GSR2:1;      /*    MSSF      */
                             unsigned char GSR1:1;      /*    SRWF      */
                             unsigned char GSR0 :1;      /*    BOF       */
                             }       BIT;               /*              */
                      }         GSR;                    /*              */
                union {                                 /* BCR1         */
                      unsigned short WORD;              /*  Word Access */
                      struct {                          /*  Bit  Access */
                             unsigned char TSEG1:4;     /*    TSEG1     */
                             unsigned char      :1;     /*              */
                             unsigned char TSEG2:3;     /*    TSEG2     */
                             unsigned char      :2;     /*              */
                             unsigned char SJW  :2;     /*    SJW       */
                             unsigned char      :3;     /*              */
                             unsigned char BSP  :1;     /*    BSP       */
                             }       BIT;               /*              */
                      }         BCR1;                   /*              */
                union {                                 /* BCR0         */
                      unsigned short WORD;              /*  Word Access */
                      struct {                          /*  Bit  Access */
                             unsigned char    :8;       /*              */
                             unsigned char BRP:8;       /*    BRP       */
                             }       BIT;               /*              */
                      }         BCR0;                   /*              */
                union {                                 /* IRR          */
                      unsigned short WORD;              /*  Word Access */
                      struct {                          /*  Bit  Access */
                             unsigned char IRR15:1;      /*    CMF1      */
                             unsigned char IRR14:1;      /*    CMF0      */
                             unsigned char IRR13:1;      /*    OVF       */
                             unsigned char IRR12:1;      /*    BSF       */
                             unsigned char     :2;      /*              */
                             unsigned char IRR9:1;      /*    UMF       */
                             unsigned char IRR8:1;      /*    MEF       */
                             unsigned char IRR7:1;      /*    OLFF      */
                             unsigned char IRR6:1;      /*    BOF       */
                             unsigned char IRR5:1;      /*    EPF       */
                             unsigned char IRR4:1;      /*    ROWF      */
                             unsigned char IRR3:1;      /*    SOWF      */
                             unsigned char IRR2:1;      /*    RFRF      */
                             unsigned char IRR1:1;      /*    RMF       */
                             unsigned char IRR0:1;      /*    RSTF      */
                             }       BIT;               /*              */
                      }         IRR;                    /*              */
                union {                                 /* IMR          */
                      unsigned short WORD;              /*  Word Access */
                      struct {                          /*  Bit  Access */
                             unsigned char IMIE1:1;     /*    IMIE1     */
                             unsigned char IMIE0:1;     /*    IMIE0     */
                             unsigned char OVIE :1;     /*    OVIE      */
                             unsigned char BSIE :1;     /*    BSIE      */
                             unsigned char      :2;     /*              */
                             unsigned char UMIE :1;     /*    UMIE      */
                             unsigned char MEIE :1;     /*    MEIE      */
                             unsigned char OLFIE:1;     /*    OLFIE     */
                             unsigned char BOIE :1;     /*    BOIE      */
                             unsigned char EPIE :1;     /*    EPIE      */
                             unsigned char ROWIE:1;     /*    ROWIE     */
                             unsigned char SOWIE:1;     /*    SOWIE     */
                             unsigned char RFRIE:1;     /*    RFRIE     */
                             unsigned char RMIE :1;     /*    RMIE      */
                             }       BIT;               /*              */
                      }         IMR;                    /*              */
                unsigned char   TEC;                    /* TEC          */
                unsigned char   REC;                    /* REC          */
                char            wk1[18];                /*              */
                union un_mb31_1 TXPR;                   /* TXPR         */
                char            wk2[4];                 /*              */
                union un_mb31_1 TXCR;                   /* TXCR         */
                char            wk3[4];                 /*              */
                union un_mb31_1 TXACK;                  /* TXACK        */
                char            wk4[4];                 /*              */
                union un_mb31_1 ABACK;                  /* ABACK        */
                char            wk5[4];                 /*              */
                union un_mb31_0 RXPR;                   /* RXPR         */
                char            wk6[4];                 /*              */
                union un_mb31_0 RFPR;                   /* RFPR         */
                char            wk7[4];                 /*              */
                union un_mb31_0 MBIMR;                  /* MBIMR        */
                char            wk8[4];                 /*              */
                union un_mb31_0 UMSR;                   /* UMSR         */
                char            wk9[36];                /*              */
                unsigned short  TCNTR;                  /* TCNTR        */
                union {                                 /* TCR          */
                      unsigned short WORD;              /*  Word Access */
                      struct {                          /*  Bit  Access */
                             unsigned char ET    :1;    /*    ET        */
                             unsigned char DICR0 :1;    /*    DICR0     */
                             unsigned char RTSC  :1;    /*    RTSC      */
                             unsigned char STSC  :1;    /*    STSC      */
                             unsigned char TTCSC :1;    /*    TTCSC     */
                             unsigned char CTCSC :1;    /*    CTCSC     */
                             unsigned char ICR0AD:1;    /*    ICR0AD    */
                             unsigned char SCS   :1;    /*    SCS       */
                             unsigned char DCC   :1;    /*    DCC       */
                             unsigned char       :1;    /*              */
                             unsigned char TPSC :6;     /*    TPSC      */
                             }       BIT;               /*              */
                      }         TCR;                    /*              */
                union {                                 /* TSR          */
                      unsigned short WORD;              /*  Word Access */
                      struct {                          /*  Bit  Access */
                             unsigned char     :8;      /*              */
                             unsigned char     :5;      /*              */
                             unsigned char CMF1:1;      /*    CMF1      */
                             unsigned char CMF0:1;      /*    CMF0      */
                             unsigned char OVF :1;      /*    OVF       */
                             }       BIT;               /*              */
                      }         TSR;                    /*              */
                unsigned short  TDCR;                   /* TDCR         */
                unsigned short  LOSR;                   /* LOSR         */
                char            wk10[2];                /*              */
                unsigned short  ICR0;                   /* ICR0         */
                unsigned short  ICR1;                   /* ICR1         */
                unsigned short  TCMR0;                  /* TCMR0        */
                unsigned short  TCMR1;                  /* TCMR1        */
                char            wk11[108];              /*              */
                struct {                                /* MB           */
                 union {                                /* Control(CTRL)*/
                       unsigned int LONG;               /*  Long Access */
                       struct {                         /*  Bit  Access */
                              unsigned int      : 1;    /*              */
                              unsigned int STID :11;    /*    STDID     */
                              unsigned int RTR  : 1;    /*    RTR       */
                              unsigned int IDE  : 1;    /*    IDE       */
                              unsigned int EXTID:18;    /*    EXTID     */
                               }    BIT;                /*              */
                       }           CTRLH;               /*              */
                 union {                                /* Control(CTRL)*/
                       unsigned short WORD;             /*  Word Access */
                       struct {                         /*  Bit  Access */
                              unsigned char CCM :1;     /*    CCM       */
                              unsigned char TTE :1;     /*    TTE       */
                              unsigned char NMC :1;     /*    NMC       */
                              unsigned char ATX :1;     /*    ATX       */
                              unsigned char DART:1;     /*    DART      */
                              unsigned char MBC :3;     /*    MBC       */
                              unsigned char PTE :1;     /*    PTE       */
                              unsigned char TCT :1;     /*    TCT       */
                              unsigned char CBE :1;     /*    CBE       */
                              unsigned char     :1;     /*              */
                              unsigned char DLC :4;     /*    DLC       */
                              }       BIT;              /*              */
                       }           CTRLL;               /*              */
                 unsigned short    TMSTP;               /* TimeStamp    */
                 unsigned char     MSG_DATA[8];         /* MSG_DATA     */
                 union {                                /* LAFM         */
                       unsigned int   LONG;             /*  Long Access */
                       unsigned short TTT;              /*  TTT  Access */
                       struct {                         /*  Bit  Access */
                              unsigned int       : 1;   /*              */
                              unsigned int  STID :11;   /*    STDID     */
                              unsigned int       : 2;   /*              */
                              unsigned int  EXTID:18;   /*    EXTID     */
                              }       BIT;              /*              */
                       }           LAFM;                /*              */
                 char              wk[12];              /*              */
                }               MB[32];                 /*              */
};                                                      /*              */                                                      /*              */
#define SCI2  (*(volatile struct st_sci   *)0xFFFF81C0) /* SCI2  Address*/
#define SCI3  (*(volatile struct st_sci   *)0xFFFF81D0) /* SCI3  Address*/
#define SCI4  (*(volatile struct st_sci   *)0xFFFF81E0) /* SCI4  Address*/
#define MTU   (*(volatile struct st_mtu   *)0xFFFF820A) /* MTU   Address*/
#define MTU0  (*(volatile struct st_mtu0  *)0xFFFF8260) /* MTU0  Address*/
#define MTU1  (*(volatile struct st_mtu1  *)0xFFFF8280) /* MTU1  Address*/
#define MTU2  (*(volatile struct st_mtu1  *)0xFFFF82A0) /* MTU2  Address*/
#define MTU3  (*(volatile struct st_mtu3  *)0xFFFF8200) /* MTU3  Address*/
#define MTU4  (*(volatile struct st_mtu4  *)0xFFFF8200) /* MTU4  Address*/
#define POE   (*(volatile struct st_poe   *)0xFFFF83C0) /* POE   Address*/
#define INTC  (*(volatile struct st_intc  *)0xFFFF8348) /* INTC  Address*/
#define PA    (*(volatile struct st_pa    *)0xFFFF8382) /* PA    Address*/
#define PB    (*(volatile struct st_pb    *)0xFFFF8390) /* PB    Address*/
#define PD    (*(volatile struct st_pd    *)0xFFFF83A2) /* PD    Address*/
#define PE    (*(volatile struct st_pe    *)0xFFFF83B0) /* PE    Address*/
#define PF    (*(volatile struct st_pf    *)0xFFFF83B2) /* PF    Address*/
#define PFC   (*(volatile struct st_pfc   *)0xFFFF8386) /* PFC   Address*/
#define CMT   (*(volatile struct st_cmt   *)0xFFFF83D0) /* CMT   Address*/
#define CMT0  (*(volatile struct st_cmt0  *)0xFFFF83D2) /* CMT0  Address*/
#define CMT1  (*(volatile struct st_cmt0  *)0xFFFF83D8) /* CMT1  Address*/
#define AD0   (*(volatile struct st_ad0   *)0xFFFF8420) /* A/D0  Address*/
#define AD1   (*(volatile struct st_ad1   *)0xFFFF8428) /* A/D1  Address*/
#define FLASH (*(volatile struct st_flash *)0xFFFF8580) /* FLASH Address*/
#define UBC   (*(volatile struct st_ubc   *)0xFFFF8600) /* UBC   Address*/
#define WDT   (*(volatile union  un_wdt   *)0xFFFF8610) /* WDT   Address*/
#define SBYCR (*(volatile union  un_sbycr *)0xFFFF8614) /* SBYCR Address*/
#define SYSCR (*(volatile union  un_syscr *)0xFFFF8618) /* SYSCR Address*/
#define MST   (*(volatile struct st_mst   *)0xFFFF861C) /* MST   Address*/
#define BSC   (*(volatile struct st_bsc   *)0xFFFF8620) /* BSC   Address*/
#define DTC   (*(volatile struct st_dtc   *)0xFFFF8700) /* DTC   Address*/
#define MMT   (*(volatile struct st_mmt   *)0xFFFF8A00) /* MMT   Address*/
#define PWM   (*(volatile struct st_pwm   *)0xFFFF8A00) /* PWM   Address*/
#define PWMU  (*(volatile struct st_pwmu  *)0xFFFF8A10) /* PWMU  Address*/
#define PWMV  (*(volatile struct st_pwmv  *)0xFFFF8A20) /* PWMV  Address*/
#define PWMW  (*(volatile struct st_pwmw  *)0xFFFF8A30) /* PWMW  Address*/
#define HUDI  (*(volatile struct st_hudi  *)0xFFFF8A50) /* H-UDI Address*/
#define HCAN2 (*(volatile struct st_hcan2 *)0xFFFFB000) /* HCAN2 Address*/
