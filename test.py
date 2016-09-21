from SampleHelper import SampleManager
import ROOT
import logging
import numpy as np
import HGCalHelpers


def getRecHitDetIds(rechits):
    recHitsList = []
    for rHit in rechits:
        recHitsList.append(rHit.detid)
    # print "RecHits -"*10
    # print recHitsList
    recHits = np.array(recHitsList)
    return recHits


def getHitList(simClus, recHitDetIds):
    sClusHitsList = []
    for DetId in simClus.hits:
        sClusHitsList.append(DetId)
    # print sClusHitsList
    sClusHits = np.array(sClusHitsList)
    # thanks to http://stackoverflow.com/questions/11483863/python-intersection-indices-numpy-array
    recHitIndices = np.nonzero(np.in1d(recHitDetIds, sClusHits))
    # print "indices - "*10
    # print recHitIndices
    # if (len(recHitIndices[0]) != len(sClusHitsList)):
        # print "Mismatch:", len(recHitIndices[0]), len(sClusHits)
    return recHitIndices


def getHists():
    histDict = {}
    clusters = ["SimClus", "PFClus", "GenPart", "RecHits", "RecHitsClus"]
    for clus in clusters:

        histDict["%s_energy" %clus] = ROOT.TH1F("%s_energy" %clus, "%s_energy;E [GeV]" %clus, 200, 0, 100)
        histDict["%s_pt" %clus] = ROOT.TH1F("%s_pt" %clus, "%s_pt;p_{T} [GeV]" %clus, 100, 0, 25)
        histDict["%s_eta" %clus] = ROOT.TH1F("%s_eta" %clus, "%s_eta;#eta" %clus, 100, -5, 5)
        histDict["%s_phi" %clus] = ROOT.TH1F("%s_phi" %clus, "%s_phi;#phi" %clus, 100, -3.2, 3.2)
        if (clus == "SimClus"):
            histDict["%s_energy_pass" %clus] = ROOT.TH1F("%s_energy_pass" %clus, "%s_energy_pass;E [GeV]" %clus, 200, 0, 100)
            histDict["%s_pt_pass" %clus] = ROOT.TH1F("%s_pt_pass" %clus, "%s_pt_pass;p_{T} [GeV]" %clus, 100, 0, 25)
            histDict["%s_eta_pass" %clus] = ROOT.TH1F("%s_eta_pass" %clus, "%s_eta;_pass;#eta" %clus, 100, -5, 5)
            histDict["%s_phi_pass" %clus] = ROOT.TH1F("%s_phi_pass" %clus, "%s_phi_pass;#phi" %clus, 100, -3.2, 3.2)
            histDict["%s_simEnergy" %clus] = ROOT.TH1F("%s_simEnergy" %clus, "%s_simEnergy;simE [GeV]" %clus, 200, 0, 50)
            histDict["%s_layers_energy" %clus] = ROOT.TH2F("%s_layers_energy" %clus, "%s_layers_energy;layers;energy [GeV]" %clus, 30, 0, 30, 200, 0, 50)
            histDict["%s_cells_energy" %clus] = ROOT.TH2F("%s_cells_energy" %clus, "%s_cells_energy;cells;energy [GeV]" %clus, 245, 0, 245, 200, 0, 50)
            histDict["%s_wafers_energy" %clus] = ROOT.TH2F("%s_wafers_energy" %clus, "%s_wafers_energy;wafer;energy [GeV]" %clus, 550, 0, 550, 200, 0, 50)
            histDict["%s_fractions_energy" %clus] = ROOT.TH2F("%s_fractions_energy" %clus, "%s_fractions_energy;fraction;energy [GeV]" %clus, 100, 0, 1, 200, 0, 50)
            histDict["%s_layers_pt" %clus] = ROOT.TH2F("%s_layers_pt" %clus, "%s_layers_pt;layers;p_{T} [GeV]" %clus, 30, 0, 30, 200, 0, 50)
            histDict["%s_cells_pt" %clus] = ROOT.TH2F("%s_cells_pt" %clus, "%s_cells_pt;cells;p_{T} [GeV]" %clus, 245, 0, 245, 200, 0, 50)
            histDict["%s_wafers_pt" %clus] = ROOT.TH2F("%s_wafers_pt" %clus, "%s_wafers_pt;wafer;p_{T} [GeV]" %clus, 550, 0, 550, 200, 0, 50)
            histDict["%s_fractions_pt" %clus] = ROOT.TH2F("%s_fractions_pt" %clus, "%s_fractions_pt;fraction;p_{T} [GeV]" %clus, 100, 0, 1, 200, 0, 50)
            histDict["%s_layers_fractions" %clus] = ROOT.TH2F("%s_layers_fractions" %clus, "%s_layers_fractions;layers;fractions" %clus, 30, 0, 30, 100, 0, 1)
            histDict["%s_cells_fractions" %clus] = ROOT.TH2F("%s_cells_fractions" %clus, "%s_cells_fractions;cells;fractions" %clus, 245, 0, 245, 100, 0, 1)
            histDict["%s_wafers_fractions" %clus] = ROOT.TH2F("%s_wafers_fractions" %clus, "%s_wafers_fractions;wafer;fractions" %clus, 550, 0, 550, 100, 0, 1)

        if (clus == "GenPart"):
            histDict["%s_dvz" %clus] = ROOT.TH1F("%s_dvz" %clus, "%s_dvz;dvz [cm]" %clus, 100, -500, 500)

        if (clus.find("RecHits") >= 0):
            histDict["%s_layers_energy" %clus] = ROOT.TH2F("%s_layers_energy" %clus, "%s_layers_energy;layers;energy [GeV]" %clus, 40, 0.5, 40.5, 200, 0, 30)
            histDict["%s_layers_pt" %clus] = ROOT.TH2F("%s_layers_pt" %clus, "%s_layers_pt;layers;p_{T} [GeV]" %clus, 40, 0.5, 40.5, 200, 0, 10)
            histDict["%s_layers_eta" %clus] = ROOT.TH2F("%s_layers_eta" %clus, "%s_layers_eta;layers;#eta" %clus, 40, 0.5, 40.5, 100, -5, 5)

        histDict["%s_dRtoSeed" %clus] = ROOT.TH1F(
            "%s_dRtoSeed" %clus, "%s_dRtoSeed;#Delta R to seed" %clus, 100, -0.2, 0.2)

        if (clus != "GenPart"):
            histDict["multi%s_energy" %clus] = ROOT.TH1F("multi%s_energy" %clus, "multi%s_energy;E [GeV]" %clus, 200, 0, 50)
            histDict["multi%s_pt" %clus] = ROOT.TH1F("multi%s_pt" %clus, "multi%s_pt;p_{T} [GeV]" %clus, 100, 0, 10)
            histDict["multi%s_eta" %clus] = ROOT.TH1F("multi%s_eta" %clus, "multi%s_eta;#eta" %clus, 100, -5, 5)
            histDict["multi%s_phi" %clus] = ROOT.TH1F("multi%s_phi" %clus, "multi%s_phi;#phi" %clus, 100, -3.2, 3.2)

    compClusters = ["SimVsPF", "GenVsPF", "GenVsSim", "SimVsRecHits"]
    for comp in compClusters:
        if comp.find("Gen") < 0:
            histDict["%s_delta_energy" %comp] = ROOT.TH1F("%s_delta_energy" %comp, "%s_delta_energy;#Delta E [GeV]" %comp, 100, -20, 40)
            histDict["%s_delta_pt" %comp] = ROOT.TH1F("%s_delta_pt" %comp, "%s_delta_pt;#Delta p_{T} [GeV]" %comp, 100, -10, 20)
            histDict["%s_deltaover_energy" %comp] = ROOT.TH1F("%s_deltaover_energy" %comp, "%s_delta_overenergy;#Delta E/E" %comp, 100, -1, 1)
            histDict["%s_deltaover_pt" %comp] = ROOT.TH1F("%s_deltaover_pt" %comp, "%s_deltaover_pt;#Delta p_{T}/p_{T}" %comp, 100, -1, 1)
            histDict["%s_delta_eta" %comp] = ROOT.TH1F("%s_delta_eta" %comp, "%s_delta_eta;#Delta #eta" %comp, 100, -1, 1)
            histDict["%s_delta_phi" %comp] = ROOT.TH1F("%s_delta_phi" %comp, "%s_delta_phi;#Delta #phi" %comp, 100, -1, 1)
            histDict["%s_delta_R" %comp] = ROOT.TH1F("%s_delta_R" %comp, "%s_delta_R;#Delta R" %comp, 100, -1, 1)

        histDict["multi%s_delta_energy" %comp] = ROOT.TH1F("multi%s_delta_energy" %comp, "multi%s_delta_energy;#Delta E [GeV]" %comp, 100, -10, 10)
        histDict["multi%s_delta_pt" %comp] = ROOT.TH1F("multi%s_delta_pt" %comp, "multi%s_delta_pt;#Delta p_{T} [GeV]" %comp, 100, -5, 5)
        histDict["multi%s_deltaover_energy" %comp] = ROOT.TH1F("multi%s_deltaover_energy" %comp, "multi%s_deltaover_energy;#Delta E/E" %comp, 100, -5, 5)
        histDict["multi%s_deltaover_pt" %comp] = ROOT.TH1F("multi%s_deltaover_pt" %comp, "multi%s_deltaover_pt;#Delta p_{T}/p_{T}" %comp, 100, -5, 5)
        histDict["multi%s_delta_eta" %comp] = ROOT.TH1F("multi%s_delta_eta" %comp, "multi%s_delta_eta;#Delta #eta" %comp, 100, -1, 1)
        histDict["multi%s_delta_phi" %comp] = ROOT.TH1F("multi%s_delta_phi" %comp, "multi%s_delta_phi;#Delta #phi" %comp, 100, -1, 1)
        histDict["multi%s_delta_R" %comp] = ROOT.TH1F("multi%s_delta_R" %comp, "multi%s_delta_R;#Delta R" %comp, 100, -1, 1)
        histDict["multi%s_eff" %comp] = ROOT.TH1F("multi%s_eff" %comp, "multi%s_eff;eff." %comp, 2, -0.5, 1.5)

        if comp.find("Gen") < 0:
            histDict["multi%s_selected_delta_energy" %comp] = ROOT.TH1F("multi%s_selected_delta_energy" %comp, "multi%s_selected_delta_energy;#Delta E [GeV]" %comp, 100, -10, 10)
            histDict["multi%s_selected_delta_pt" %comp] = ROOT.TH1F("multi%s_selected_delta_pt" %comp, "multi%s_selected_delta_pt;#Delta p_{T} [GeV]" %comp, 100, -5, 5)
            histDict["multi%s_selected_deltaover_energy" %comp] = ROOT.TH1F("multi%s_selected_deltaover_energy" %comp, "multi%s_selected_deltaover_energy;#Delta E/E" %comp, 100, -10, 10)
            histDict["multi%s_selected_deltaover_pt" %comp] = ROOT.TH1F("multi%s_selected_deltaover_pt" %comp, "multi%s_selected_deltaover_pt;#Delta p_{T}/p_{T}" %comp, 100, -5, 5)
            histDict["multi%s_selected_delta_eta" %comp] = ROOT.TH1F("multi%s_selected_delta_eta" %comp, "multi%s_selected_delta_eta;#Delta #eta" %comp, 100, -1, 1)
            histDict["multi%s_selected_delta_phi" %comp] = ROOT.TH1F("multi%s_selected_delta_phi" %comp, "multi%s_selected_delta_phi;#Delta #phi" %comp, 100, -1, 1)
            histDict["multi%s_selected_delta_R" %comp] = ROOT.TH1F("multi%s_selected_delta_R" %comp, "multi%s_selected_delta_R;#Delta R" %comp, 100, -1, 1)
            histDict["multi%s_selected_eff" %comp] = ROOT.TH1F("multi%s_selected_eff" %comp, "multi%s_selected_eff;eff." %comp, 2, -0.5, 1.5)
        if comp == "SimVsRecHits":
            detectors = ["EE", "FH", "both"]
            etaRanges = ["fullEta", "1p70_1p95", "1p95_2p20", "2p20_2p45", "2p45_2p70"]
            for detect in detectors:
                for etaR in etaRanges:
                    histDict["%s_delta_energy_%s_%s" %(comp, detect, etaR)] = ROOT.TH1F("%s_delta_energy_%s_%s" %(comp, detect, etaR), "%s_delta_energy_%s_%s;#Delta E [GeV]" %(comp, detect, etaR), 100, -20, 20)
                    histDict["%s_delta_pt_%s_%s" %(comp, detect, etaR)] = ROOT.TH1F("%s_delta_pt_%s_%s" %(comp, detect, etaR), "%s_delta_pt_%s_%s;#Delta p_{T} [GeV]" %(comp, detect, etaR), 100, -10, 10)
                    histDict["%s_deltaover_energy_%s_%s" %(comp, detect, etaR)] = ROOT.TH1F("%s_deltaover_energy_%s_%s" %(comp, detect, etaR), "%s_delta_overenergy_%s_%s;#Delta E/E" %(comp, detect, etaR), 100, -1, 1)
                    histDict["%s_deltaover_pt_%s_%s" %(comp, detect, etaR)] = ROOT.TH1F("%s_deltaover_pt_%s_%s" %(comp, detect, etaR), "%s_deltaover_pt_%s_%s;#Delta p_{T}/p_{T}" %(comp, detect, etaR), 100, -1, 1)
                    histDict["%s_frac_energy_%s_%s" %(comp, detect, etaR)] = ROOT.TH1F("%s_frac_energy_%s_%s" %(comp, detect, etaR), "%s_frac_energy_%s_%s;E fraction" %(comp, detect, etaR), 100, 0, 2)
                    histDict["%s_frac_pt_%s_%s" %(comp, detect, etaR)] = ROOT.TH1F("%s_frac_pt_%s_%s" %(comp, detect, etaR), "%s_frac_pt_%s_%s;p_{T} fraction" %(comp, detect, etaR), 100, 0, 2)
                    histDict["%s_frac_energy_EE_%s_%s" %(comp, detect, etaR)] = ROOT.TH2F("%s_frac_energy_EE_%s_%s" %(comp, detect, etaR), "%s_frac_energy_EE_%s_%s;E fraction EE;E fraction %s" %(comp, detect, etaR, detect), 100, 0, 2, 100, 0, 2)
                    histDict["%s_frac_pt_EE_%s_%s" %(comp, detect, etaR)] = ROOT.TH2F("%s_frac_pt_EE_%s_%s" %(comp, detect, etaR), "%s_frac_pt_EE_%s_%s;p_{T} fraction EE;p_{T} fraction %s" %(comp, detect, etaR, detect), 100, 0, 2, 100, 0, 2)
                    histDict["%s_frac_energy_eta_%s_%s" %(comp, detect, etaR)] = ROOT.TH2F("%s_frac_energy_eta_%s_%s" %(comp, detect, etaR), "%s_frac_energy_eta_%s_%s;E fraction;RecHits cluster #eta" %(comp, detect, etaR), 100, 0, 2, 100, -5, 5)
                    histDict["%s_frac_pt_eta_%s_%s" %(comp, detect, etaR)] = ROOT.TH2F("%s_frac_pt_eta_%s_%s" %(comp, detect, etaR), "%s_frac_pt_eta_%s_%s;p_{T} fraction;RecHits cluster #eta" %(comp, detect, etaR), 100, 0, 2, 100, -5, 5)

    return histDict



def main():

    localTest = False
    nEvents = -1
    dvzCut = -1000  # 320
    simClusPtCut = 16
    imgType = "pdf"
    applyRecHitsRelPtCut = False
    outDir = "singlePions"
    if not applyRecHitsRelPtCut:
        outDir = "singlePions_noRelPtCut"

    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(message)s')
    ch.setFormatter(formatter)

    sampleManager = SampleManager()
    sample = sampleManager.getSample("chargedPions_nPart1_Pt20")
    chain = sample.getChain()
    if localTest:
        inFile = ROOT.TFile.Open("/afs/cern.ch/user/c/clange/work/HGCal/ntupliser/CMSSW_8_1_0_pre8/src/RecoNtuples/HGCalAnalysis/test/twogamma_pt5_eta2_nosmear_calib_ntuple.root")
        chain = inFile.Get("ana/hgc")

    HGCalHelpers.createOutputDir(outDir)
    histDict = getHists()
    canvas = ROOT.TCanvas(outDir, outDir, 500, 500)

    sampleEvents = chain.GetEntries()
    logger.info("Events: %d" % sampleEvents)

    # start event loop
    for currentEvent, event in enumerate(chain):
        if (currentEvent % 100 == 0):
            logger.info("Event {} of {}".format(currentEvent, sampleEvents))

        # associate RecHits to SimClusters
        simClusHitAssoc = []
        recHitDetIds = getRecHitDetIds(event.rechits_raw)
        for simClusIndex,simClus in enumerate(event.simcluster):
            # print ("SimClus %d - "%simClusIndex)*10
            simClusHitAssoc.append(getHitList(simClus, recHitDetIds))

        # get generator particles applying conversion cut
        vGenParticleTLV = HGCalHelpers.getGenParticles(event, histDict, dvzCut)

        # keep track of SimClusters that are in the same hemisphere as the selected GenParticles
        matchesGen = [False]*len(event.simcluster)

        simClusIndex = 0
        for simCl, pfCl in zip(event.simcluster, event.pfcluster):
            # logging.info("{} {}".format(simCl.pt, pfCl.pt))
            for genPartIndex, genPart in enumerate(vGenParticleTLV):
                # if deltaR2(genPart, simCl) < loose_dRCut:
                if genPart.Eta()*simCl.eta  > 0:
                    matchesGen[simClusIndex] = True
                    histDict["SimVsPF_delta_energy"].Fill(simCl.energy-pfCl.energy)
                    histDict["SimVsPF_delta_pt"].Fill(simCl.pt-pfCl.pt)
                    histDict["SimVsPF_deltaover_energy"].Fill((simCl.energy-pfCl.energy)/simCl.energy)
                    histDict["SimVsPF_deltaover_pt"].Fill((simCl.pt-pfCl.pt)/simCl.pt)
                    histDict["SimVsPF_delta_eta"].Fill(simCl.eta-pfCl.eta)
                    histDict["SimVsPF_delta_phi"].Fill(simCl.phi-pfCl.phi)
                    histDict["SimVsPF_delta_R"].Fill(HGCalHelpers.deltaR(simCl, pfCl))
                    break
            simClusIndex += 1

        # use the SimClusters that "match" the GenParticles and study associated RecHits
        detectors = ["EE", "FH", "both"]
        for simClusIndex, simCl in enumerate(event.simcluster):
            histDict["SimClus_energy"].Fill(simCl.energy)
            histDict["SimClus_pt"].Fill(simCl.pt)
            histDict["SimClus_eta"].Fill(simCl.eta)
            histDict["SimClus_phi"].Fill(simCl.phi)
            # if (matchesGen[simClusIndex]):
            if (simCl.pt >= simClusPtCut) and not ((abs(simCl.eta) < 1.7) or (abs(simCl.eta) > 2.7)):
                histDict["SimClus_energy_pass"].Fill(simCl.energy)
                histDict["SimClus_pt_pass"].Fill(simCl.pt)
                histDict["SimClus_eta_pass"].Fill(simCl.eta)
                histDict["SimClus_phi_pass"].Fill(simCl.phi)
                recHitVectors = {}
                recHitVectorsLayer = {}
                for detect in detectors:
                    recHitVectors[detect] = ROOT.TLorentzVector()
                for layer in range(1,41):
                    recHitVectorsLayer[layer] = ROOT.TLorentzVector()
                for hitIndexArray in simClusHitAssoc[simClusIndex]:
                    for hitIndex in hitIndexArray:
                        thisHit = event.rechits_raw[hitIndex]
                        # print thisHit.energy
                        histDict["RecHits_layers_energy"].Fill(thisHit.layer, thisHit.energy)
                        histDict["RecHits_layers_pt"].Fill(thisHit.layer, thisHit.pt)
                        histDict["RecHits_layers_eta"].Fill(thisHit.layer, thisHit.eta)
                        recHitTLV = ROOT.TLorentzVector()
                        recHitTLV.SetPtEtaPhiE(thisHit.pt, thisHit.eta, thisHit.phi, thisHit.energy)
                        recHitVectors["both"] += recHitTLV
                        recHitVectorsLayer[thisHit.layer] += recHitTLV
                        if (thisHit.layer < 29):
                            recHitVectors["EE"] += recHitTLV
                        else:
                            recHitVectors["FH"] += recHitTLV
                logger.debug("SimCluster pt, E: {}, {} - RecHitVector pt, E: {}, {}".format(simCl.pt, simCl.energy, recHitVectors["both"].Pt(), recHitVectors["both"].E()))
                relative pT cut to clean up misreconstructed particles
                if applyRecHitsRelPtCut:
                    if (recHitVectors["both"].Pt() < 0.8*simCl.pt):
                        continue
                histDict["RecHits_energy"].Fill(recHitVectors["both"].E())
                histDict["RecHits_eta"].Fill(recHitVectors["both"].Eta())
                histDict["RecHits_phi"].Fill(recHitVectors["both"].Phi())
                histDict["RecHits_pt"].Fill(recHitVectors["both"].Pt())
                histDict["SimVsRecHits_delta_eta"].Fill(simCl.eta-recHitVectors["both"].Eta())
                histDict["SimVsRecHits_delta_phi"].Fill(simCl.phi-recHitVectors["both"].Phi())
                for layer, thisHit in recHitVectorsLayer.items():
                    if (thisHit.E() > 0):
                        histDict["RecHitsClus_layers_energy"].Fill(layer, thisHit.E())
                        histDict["RecHitsClus_layers_pt"].Fill(layer, thisHit.Pt())
                        histDict["RecHitsClus_layers_eta"].Fill(layer, thisHit.Eta())
                # histDict["SimVsRecHits_delta_R"].Fill(HGCalHelpers.deltaR(simCl, recHitVector))
                for detect in detectors:
                    etaR = "fullEta"
                    histDict["SimVsRecHits_delta_energy_%s_%s" % (detect, etaR)].Fill(simCl.energy-recHitVectors[detect].E())
                    histDict["SimVsRecHits_delta_pt_%s_%s" % (detect, etaR)].Fill(simCl.pt-recHitVectors[detect].Pt())
                    histDict["SimVsRecHits_deltaover_energy_%s_%s" % (detect, etaR)].Fill((simCl.energy-recHitVectors[detect].E())/simCl.energy)
                    histDict["SimVsRecHits_deltaover_pt_%s_%s" % (detect, etaR)].Fill((simCl.pt-recHitVectors[detect].Pt())/simCl.pt)
                    histDict["SimVsRecHits_frac_energy_%s_%s" % (detect, etaR)].Fill(recHitVectors[detect].E()/simCl.energy)
                    histDict["SimVsRecHits_frac_pt_%s_%s" % (detect, etaR)].Fill(recHitVectors[detect].Pt()/simCl.pt)
                    histDict["SimVsRecHits_frac_energy_EE_%s_%s" % (detect, etaR)].Fill(recHitVectors["EE"].E()/simCl.energy, recHitVectors[detect].E()/simCl.energy)
                    histDict["SimVsRecHits_frac_pt_EE_%s_%s" % (detect, etaR)].Fill(recHitVectors["EE"].Pt()/simCl.pt, recHitVectors[detect].Pt()/simCl.pt)
                    histDict["SimVsRecHits_frac_energy_eta_%s_%s" % (detect, etaR)].Fill(recHitVectors[detect].E()/simCl.energy, recHitVectors[detect].Eta())
                    histDict["SimVsRecHits_frac_pt_eta_%s_%s" % (detect, etaR)].Fill(recHitVectors[detect].Pt()/simCl.pt, recHitVectors[detect].Eta())
                    if (abs(simClus.eta) <= 1.95):
                        etaR = "1p70_1p95"
                    elif (abs(simClus.eta) <= 2.2):
                        etaR = "1p95_2p20"
                    elif (abs(simClus.eta) <= 2.45):
                        etaR = "2p20_2p45"
                    else:
                        etaR = "2p45_2p70"
                    histDict["SimVsRecHits_delta_energy_%s_%s" % (detect, etaR)].Fill(simCl.energy-recHitVectors[detect].E())
                    histDict["SimVsRecHits_delta_pt_%s_%s" % (detect, etaR)].Fill(simCl.pt-recHitVectors[detect].Pt())
                    histDict["SimVsRecHits_deltaover_energy_%s_%s" % (detect, etaR)].Fill((simCl.energy-recHitVectors[detect].E())/simCl.energy)
                    histDict["SimVsRecHits_deltaover_pt_%s_%s" % (detect, etaR)].Fill((simCl.pt-recHitVectors[detect].Pt())/simCl.pt)
                    histDict["SimVsRecHits_frac_energy_%s_%s" % (detect, etaR)].Fill(recHitVectors[detect].E()/simCl.energy)
                    histDict["SimVsRecHits_frac_pt_%s_%s" % (detect, etaR)].Fill(recHitVectors[detect].Pt()/simCl.pt)
                    histDict["SimVsRecHits_frac_energy_EE_%s_%s" % (detect, etaR)].Fill(recHitVectors["EE"].E()/simCl.energy, recHitVectors[detect].E()/simCl.energy)
                    histDict["SimVsRecHits_frac_pt_EE_%s_%s" % (detect, etaR)].Fill(recHitVectors["EE"].Pt()/simCl.pt, recHitVectors[detect].Pt()/simCl.pt)
                    histDict["SimVsRecHits_frac_energy_eta_%s_%s" % (detect, etaR)].Fill(recHitVectors[detect].E()/simCl.energy, recHitVectors[detect].Eta())
                    histDict["SimVsRecHits_frac_pt_eta_%s_%s" % (detect, etaR)].Fill(recHitVectors[detect].Pt()/simCl.pt, recHitVectors[detect].Eta())


        if (nEvents > 0 and currentEvent >= nEvents):
            break
    histDict["SimClus_eta_eff"] = ROOT.TGraphAsymmErrors(histDict["SimClus_eta_pass"].Clone("SimClus_eta_eff"))
    histDict["SimClus_eta_eff"].Divide(histDict["SimClus_eta_pass"], histDict["SimClus_eta"], "cl=0.683 b(1,1) mode")
    histDict["SimClus_eta_eff"].GetYaxis().SetTitle("eff.")
    HGCalHelpers.saveHistograms(histDict, canvas, outDir, imgType, logScale=False)



if __name__ == '__main__':
    main()
